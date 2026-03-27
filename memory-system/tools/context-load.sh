#!/usr/bin/env bash
# context-load.sh — Tiered Context Loader
#
# Implements progressive disclosure: loads only what's needed for the current
# wave depth, adapted for Buildr's architecture.
#
# Tiers (architecture always included):
#   hot  — Architecture + wave brief + current state (~1.5K tokens). Fast start.
#   warm — Hot + handoff + distilled + MEMORY.md (~3-4K tokens). Default.
#   cold — Everything including full raw discoveries + vault index (~5K+ tokens).
#
# Usage:
#   context-load.sh                     # Auto-select tier based on handoff age
#   context-load.sh --tier hot          # Architecture + brief + state
#   context-load.sh --tier warm         # Standard continuation
#   context-load.sh --tier cold         # Full history
#   context-load.sh --budget 500        # Fill up to 500 tokens (knapsack)
#   context-load.sh --refresh           # Regenerate context files first
#   context-load.sh --tier hot --json   # Output as JSON instead of markdown
#
# Output: Prints the assembled context to stdout. Pipe or redirect as needed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"
CONTEXT_DIR="$MEMORY_ROOT/context"
DEFAULTS_CONFIG="$MEMORY_ROOT/config/defaults.json"

ARCHITECTURE_FILE="$WORKSPACE_ROOT/BUILDR_ARCHITECTURE.md"
WAVE_BRIEF_FILE="$CONTEXT_DIR/wave-brief.md"
HANDOFF_FILE="$CONTEXT_DIR/handoff.md"
DISTILLED_FILE="$CONTEXT_DIR/distilled.md"
DISCOVERIES_FILE="$MEMORY_ROOT/continuum/discoveries.jsonl"
MEMORY_MD_FILE="$WORKSPACE_ROOT/MEMORY.md"
VAULT_INDEX_FILE="$WORKSPACE_ROOT/vault/INDEX.md"
STATE_FILE="$WORKSPACE_ROOT/state/orchestration.yaml"
if [[ ! -f "$STATE_FILE" ]]; then
  STATE_FILE="$WORKSPACE_ROOT/templates/state/orchestration.yaml"
fi

# --- Defaults ---
TIER=""
REFRESH=false
FORMAT="markdown"
BUDGET=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tier)     TIER="$2";      shift 2 ;;
    --budget)   BUDGET="$2";    shift 2 ;;
    --refresh)  REFRESH=true;   shift ;;
    --json)     FORMAT="json";  shift ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# --- Smart Auto Tier Selection (when no --tier specified) ---
# Uses multiple signals: handoff age, guardrail warnings, discovery freshness.
#   hot  — handoff <2h, no critical warnings, brief exists (quick continuation)
#   warm — handoff 2-168h (standard continuation)
#   cold — handoff >168h, no handoff, or brief is stale
if [[ -z "$TIER" && "$BUDGET" -eq 0 ]]; then
  GUARDRAILS_FILE="$WORKSPACE_ROOT/vault/constraints/security.md"

  # Helper: get file mtime (cross-platform)
  _file_mtime() {
    if stat --version &>/dev/null 2>&1; then
      stat -c %Y "$1" 2>/dev/null || echo 0
    else
      stat -f %m "$1" 2>/dev/null || echo 0
    fi
  }

  NOW_EPOCH=$(date +%s)
  HANDOFF_AGE_HOURS=999
  SELECTION_REASON="default"
  BRIEF_STALE=false

  if [[ -f "$HANDOFF_FILE" ]]; then
    HANDOFF_MTIME=$(_file_mtime "$HANDOFF_FILE")
    if [[ "$HANDOFF_MTIME" -gt 0 ]]; then
      HANDOFF_AGE_HOURS=$(( (NOW_EPOCH - HANDOFF_MTIME) / 3600 ))
    fi

    # Signal 1: Check for critical/high guardrail warnings
    HAS_CRITICAL_WARNINGS=false
    if [[ -f "$GUARDRAILS_FILE" ]]; then
      if grep -qiE '(CRITICAL|security|injection|dataloss|crash)' "$GUARDRAILS_FILE" 2>/dev/null; then
        HAS_CRITICAL_WARNINGS=true
      fi
    fi

    # Signal 2: Check if brief is stale (older than latest discovery)
    BRIEF_STALE=false
    if [[ -f "$WAVE_BRIEF_FILE" && -f "$DISCOVERIES_FILE" ]]; then
      BRIEF_MTIME=$(_file_mtime "$WAVE_BRIEF_FILE")
      DISC_MTIME=$(_file_mtime "$DISCOVERIES_FILE")
      if [[ "$DISC_MTIME" -gt "$BRIEF_MTIME" ]]; then
        BRIEF_STALE=true
      fi
    fi

    # Decision tree
    if [[ "$HANDOFF_AGE_HOURS" -le 2 && "$HAS_CRITICAL_WARNINGS" == false && -f "$WAVE_BRIEF_FILE" && "$BRIEF_STALE" == false ]]; then
      TIER="hot"
      SELECTION_REASON="fresh handoff (${HANDOFF_AGE_HOURS}h), no warnings, brief current"
    elif [[ "$HANDOFF_AGE_HOURS" -le 168 ]]; then
      TIER="warm"
      SELECTION_REASON="handoff age ${HANDOFF_AGE_HOURS}h"
    else
      TIER="cold"
      SELECTION_REASON="stale handoff (${HANDOFF_AGE_HOURS}h >168h)"
    fi
  else
    TIER="cold"
    SELECTION_REASON="no handoff found"
  fi

  if [[ "$BRIEF_STALE" == true ]]; then
    REFRESH=true
    SELECTION_REASON="${SELECTION_REASON}, auto-refresh (brief stale)"
  fi

  echo "_Auto-selected tier: $TIER ($SELECTION_REASON)_" >&2
fi

# Default fallback
TIER="${TIER:-warm}"

# Validate tier
case "$TIER" in
  hot|warm|cold) ;;
  *)
    echo "ERROR: Invalid tier '$TIER' (use: hot, warm, cold)" >&2
    exit 1
    ;;
esac

# --- Auto-discovery on refresh ---
if [[ "$REFRESH" == true && -f "$SCRIPT_DIR/discovery-mine.sh" ]]; then
  bash "$SCRIPT_DIR/discovery-mine.sh" > /dev/null 2>&1 || true
fi

# --- Refresh context files if requested or missing ---
if [[ "$REFRESH" == true ]] || [[ ! -f "$WAVE_BRIEF_FILE" ]]; then
  if [[ -x "$SCRIPT_DIR/wave-brief.sh" ]]; then
    "$SCRIPT_DIR/wave-brief.sh" > "$WAVE_BRIEF_FILE" 2>/dev/null || true
  fi
fi

if [[ "$REFRESH" == true ]] || [[ ! -f "$DISTILLED_FILE" ]]; then
  if [[ -x "$SCRIPT_DIR/discovery-distill.sh" ]]; then
    "$SCRIPT_DIR/discovery-distill.sh" > "$DISTILLED_FILE" 2>/dev/null || true
  fi
fi

# --- Budget mode: fill knapsack up to N tokens ---
if [[ "$BUDGET" -gt 0 ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || _PY="python"

  export _BUILDR_BUDGET="$BUDGET"
  export _BUILDR_ARCH="$ARCHITECTURE_FILE"
  export _BUILDR_BRIEF="$WAVE_BRIEF_FILE"
  export _BUILDR_STATE="$STATE_FILE"
  export _BUILDR_HANDOFF="$HANDOFF_FILE"
  export _BUILDR_DISTILLED="$DISTILLED_FILE"
  export _BUILDR_MEMORY_MD="$MEMORY_MD_FILE"
  export _BUILDR_DISCOVERIES="$DISCOVERIES_FILE"
  export _BUILDR_VAULT_INDEX="$VAULT_INDEX_FILE"

  "$_PY" << 'PYEOF'
import os

budget = int(os.environ['_BUILDR_BUDGET'])
bytes_budget = int(budget * 3.5)

def read_file(path):
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, OSError):
        return None

chunks = [
    ("Architecture", os.environ['_BUILDR_ARCH']),
    ("Wave Brief", os.environ['_BUILDR_BRIEF']),
    ("Current State", os.environ['_BUILDR_STATE']),
    ("Handoff", os.environ['_BUILDR_HANDOFF']),
    ("Distilled Discoveries", os.environ['_BUILDR_DISTILLED']),
    ("MEMORY.md", os.environ['_BUILDR_MEMORY_MD']),
    ("Raw Discoveries", os.environ['_BUILDR_DISCOVERIES']),
    ("Vault Index", os.environ['_BUILDR_VAULT_INDEX']),
]

total_used = 0
sections_loaded = []

for name, path in chunks:
    content = read_file(path)
    if not content:
        continue
    content_bytes = len(content.encode('utf-8'))
    if total_used + content_bytes <= bytes_budget:
        print(f"## {name}")
        print()
        print(content)
        print()
        print("---")
        print()
        total_used += content_bytes
        sections_loaded.append(name)
    else:
        remaining = bytes_budget - total_used
        if remaining > 200:
            truncated = content[:remaining]
            last_nl = truncated.rfind('\n')
            if last_nl > 100:
                truncated = truncated[:last_nl]
            print(f"## {name} (truncated)")
            print()
            print(truncated)
            print()
            print("---")
            print()
            total_used += len(truncated.encode('utf-8'))
            sections_loaded.append(f"{name}*")
        break

est_tokens = total_used * 10 // 35
print(f"_Budget: {budget} tok requested, ~{est_tokens} tok used ({total_used} bytes)_")
print(f"_Sections: {', '.join(sections_loaded)}_")
PYEOF

  unset _BUILDR_BUDGET _BUILDR_ARCH _BUILDR_BRIEF _BUILDR_STATE _BUILDR_HANDOFF _BUILDR_DISTILLED _BUILDR_MEMORY_MD _BUILDR_DISCOVERIES _BUILDR_VAULT_INDEX
  exit 0
fi

# --- Assemble context based on tier ---
emit_section() {
  local title="$1"
  local file="$2"
  if [[ -f "$file" ]]; then
    if [[ "$FORMAT" == "json" ]]; then
      echo "FILE:$title:$file"
    else
      echo "## $title"
      echo ""
      cat "$file"
      echo ""
      echo "---"
      echo ""
    fi
  fi
}

# Resolve Python for JSON output
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
  PYTHON_CMD="python"
fi

if [[ "$FORMAT" == "json" && -n "$PYTHON_CMD" ]]; then
  export _BUILDR_TIER="$TIER"
  export _BUILDR_ARCH="$ARCHITECTURE_FILE"
  export _BUILDR_BRIEF="$WAVE_BRIEF_FILE"
  export _BUILDR_STATE="$STATE_FILE"
  export _BUILDR_HANDOFF="$HANDOFF_FILE"
  export _BUILDR_DISTILLED="$DISTILLED_FILE"
  export _BUILDR_MEMORY_MD="$MEMORY_MD_FILE"
  export _BUILDR_DISCOVERIES="$DISCOVERIES_FILE"
  export _BUILDR_VAULT_INDEX="$VAULT_INDEX_FILE"

  "$PYTHON_CMD" << 'PYEOF'
import json, os

tier = os.environ['_BUILDR_TIER']

def read_if_exists(path):
    try:
        with open(path, encoding='utf-8') as f:
            return f.read().strip()
    except (FileNotFoundError, OSError):
        return None

def read_discoveries(path, max_count):
    entries = []
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        pass
    return entries[-max_count:] if max_count > 0 else entries

result = {
    'tier': tier,
    'sections': {}
}

architecture = read_if_exists(os.environ['_BUILDR_ARCH'])
if architecture:
    result['sections']['architecture'] = architecture

brief = read_if_exists(os.environ['_BUILDR_BRIEF'])
if brief:
    result['sections']['wave_brief'] = brief

state = read_if_exists(os.environ['_BUILDR_STATE'])
if state:
    result['sections']['current_state'] = state

if tier in ('warm', 'cold'):
    handoff = read_if_exists(os.environ['_BUILDR_HANDOFF'])
    if handoff:
        result['sections']['handoff'] = handoff

    distilled = read_if_exists(os.environ['_BUILDR_DISTILLED'])
    if distilled:
        result['sections']['distilled_discoveries'] = distilled

    memory_md = read_if_exists(os.environ['_BUILDR_MEMORY_MD'])
    if memory_md:
        result['sections']['memory'] = memory_md

if tier == 'cold':
    discoveries = read_discoveries(os.environ['_BUILDR_DISCOVERIES'], 0)
    result['sections']['raw_discoveries'] = discoveries

    vault_index = read_if_exists(os.environ['_BUILDR_VAULT_INDEX'])
    if vault_index:
        result['sections']['vault_index'] = vault_index

total_chars = sum(len(str(v)) for v in result['sections'].values())
result['estimated_tokens'] = total_chars * 10 // 35
result['total_bytes'] = total_chars

print(json.dumps(result, indent=2, ensure_ascii=False))
PYEOF
  unset _BUILDR_TIER _BUILDR_ARCH _BUILDR_BRIEF _BUILDR_STATE _BUILDR_HANDOFF _BUILDR_DISTILLED _BUILDR_MEMORY_MD _BUILDR_DISCOVERIES _BUILDR_VAULT_INDEX
else
  echo "# Buildr Context (tier: $TIER)"
  echo ""
  echo "_Loaded: $(date -u +%Y-%m-%dT%H:%M:%SZ)_"
  echo ""

  emit_section "Architecture" "$ARCHITECTURE_FILE"
  emit_section "Wave Brief" "$WAVE_BRIEF_FILE"
  emit_section "Current State" "$STATE_FILE"

  if [[ "$TIER" == "warm" || "$TIER" == "cold" ]]; then
    emit_section "Handoff" "$HANDOFF_FILE"
    emit_section "Distilled Discoveries" "$DISTILLED_FILE"
    emit_section "MEMORY.md" "$MEMORY_MD_FILE"
  fi

  if [[ "$TIER" == "cold" ]]; then
    emit_section "Vault Index" "$VAULT_INDEX_FILE"

    if [[ -f "$DISCOVERIES_FILE" ]]; then
      echo "## Raw Discoveries (full)"
      echo ""
      echo '```jsonl'
      cat "$DISCOVERIES_FILE"
      echo '```'
      echo ""
    fi
  fi

  TOTAL_CHARS=0
  for _file in "$ARCHITECTURE_FILE" "$WAVE_BRIEF_FILE" "$STATE_FILE"; do
    [[ -f "$_file" ]] && {
      _sz=$(wc -c < "$_file" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
  done
  if [[ "$TIER" == "warm" || "$TIER" == "cold" ]]; then
    for _file in "$HANDOFF_FILE" "$DISTILLED_FILE" "$MEMORY_MD_FILE"; do
      [[ -f "$_file" ]] && {
        _sz=$(wc -c < "$_file" | tr -d ' ')
        TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
      }
    done
  fi
  if [[ "$TIER" == "cold" ]]; then
    for _file in "$VAULT_INDEX_FILE" "$DISCOVERIES_FILE"; do
      [[ -f "$_file" ]] && {
        _sz=$(wc -c < "$_file" | tr -d ' ')
        TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
      }
    done
  fi

  EST_TOKENS=$(( TOTAL_CHARS * 10 / 35 ))
  echo "_Estimated context: ~${EST_TOKENS} tokens (${TOTAL_CHARS} bytes)_"
fi
