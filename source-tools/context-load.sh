#!/usr/bin/env bash
# context-load.sh — Tiered Context Loader
#
# Implements progressive disclosure: loads only what's needed for the current
# session depth. Inspired by OpenClaw's layered memory architecture.
#
# Tiers (identity always included):
#   hot  — Identity + session brief (~1.5K tokens). Fast start.
#   warm — Hot + AGENTS.md + handoff + distilled (~3-4K tokens). Default.
#   cold — Everything including full raw discoveries (~5K+ tokens).
#
# Usage:
#   context-load.sh                     # Auto-select tier based on handoff age
#   context-load.sh --tier hot          # Identity + brief (~1.5K tokens)
#   context-load.sh --tier warm         # Standard continuation (~3-4K tokens)
#   context-load.sh --tier cold         # Full history (~5K+ tokens)
#   context-load.sh --budget 500        # Fill up to 500 tokens (knapsack)
#   context-load.sh --reflect           # Pre-summarize via cheap model (~200 tokens)
#   context-load.sh --refresh           # Regenerate all context files first
#   context-load.sh --tier hot --json   # Output as JSON instead of markdown
#
# Output: Prints the assembled context to stdout. Pipe or redirect as needed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$ULTIMA_ROOT/.." && pwd)"
CONTEXT_DIR="$ULTIMA_ROOT/context"
IDENTITY_DIR="$ULTIMA_ROOT/identity"
DEFAULTS_CONFIG="$ULTIMA_ROOT/config/defaults.json"

# --- Defaults ---
TIER=""
REFRESH=false
FORMAT="markdown"
BUDGET=0
REFLECT=false
DOMAIN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tier)     TIER="$2";      shift 2 ;;
    --budget)   BUDGET="$2";    shift 2 ;;
    --refresh)  REFRESH=true;   shift ;;
    --reflect)  REFLECT=true;   shift ;;
    --json)     FORMAT="json";  shift ;;
    --domain)   DOMAIN="$2";    shift 2 ;;
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
  HANDOFF_FILE="$CONTEXT_DIR/handoff.md"
  BRIEF_FILE="$CONTEXT_DIR/session-brief.md"
  GUARDRAILS_FILE="$ULTIMA_ROOT/skills/_guardrails.md"
  DISCOVERIES_FILE="$ULTIMA_ROOT/continuum/discoveries.jsonl"

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
    if [[ -f "$BRIEF_FILE" && -f "$DISCOVERIES_FILE" ]]; then
      BRIEF_MTIME=$(_file_mtime "$BRIEF_FILE")
      DISC_MTIME=$(_file_mtime "$DISCOVERIES_FILE")
      if [[ "$DISC_MTIME" -gt "$BRIEF_MTIME" ]]; then
        BRIEF_STALE=true
      fi
    fi

    # Decision tree
    if [[ "$HANDOFF_AGE_HOURS" -le 2 && "$HAS_CRITICAL_WARNINGS" == false && -f "$BRIEF_FILE" && "$BRIEF_STALE" == false ]]; then
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
    # No handoff exists → first session or cold start
    TIER="cold"
    SELECTION_REASON="no handoff found"
  fi

  # Auto-refresh stale brief/distilled before loading
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
if [[ "$REFRESH" == true && -f "$SCRIPT_DIR/auto-discovery.sh" ]]; then
  bash "$SCRIPT_DIR/auto-discovery.sh" > /dev/null 2>&1 || true
fi

# --- Refresh context files if requested or missing ---
if [[ "$REFRESH" == true ]] || [[ ! -f "$CONTEXT_DIR/session-brief.md" ]]; then
  # Generate session brief
  if [[ -x "$SCRIPT_DIR/session-brief.sh" ]]; then
    "$SCRIPT_DIR/session-brief.sh" > "$CONTEXT_DIR/session-brief.md" 2>/dev/null || true
  fi
fi

if [[ "$REFRESH" == true ]] || [[ ! -f "$CONTEXT_DIR/distilled.md" ]]; then
  # Generate distilled discoveries
  if [[ -x "$SCRIPT_DIR/distill-discoveries.sh" ]]; then
    "$SCRIPT_DIR/distill-discoveries.sh" > "$CONTEXT_DIR/distilled.md" 2>/dev/null || true
  fi
fi

# --- Reflection Brief: pre-summarize via cheap model ---
# Uses run.sh → haiku/flash adapter to compress warm-tier into ~200 tokens.
# This is meta-cognition: a cheap brain deciding what the expensive brain needs.
if [[ "$REFLECT" == true ]]; then
  RUN_TOOL="$SCRIPT_DIR/run.sh"
  WARM_CONTEXT=""

  # Assemble warm-tier content (identity + context)
  [[ -f "$IDENTITY_DIR/SOUL.md" ]] && WARM_CONTEXT+=$(cat "$IDENTITY_DIR/SOUL.md")$'\n\n'
  [[ -f "$IDENTITY_DIR/USER.md" ]] && WARM_CONTEXT+=$(cat "$IDENTITY_DIR/USER.md")$'\n\n'
  [[ -f "$CONTEXT_DIR/session-brief.md" ]] && WARM_CONTEXT+=$(cat "$CONTEXT_DIR/session-brief.md")$'\n\n'
  [[ -f "$CONTEXT_DIR/handoff.md" ]] && WARM_CONTEXT+=$(cat "$CONTEXT_DIR/handoff.md")$'\n\n'
  [[ -f "$CONTEXT_DIR/distilled.md" ]] && WARM_CONTEXT+=$(cat "$CONTEXT_DIR/distilled.md")

  if [[ -n "$WARM_CONTEXT" && -x "$RUN_TOOL" ]]; then
    REFLECT_PROMPT="Du får kontexten från ett AI-agentsystem. Sammanfatta det viktigaste i MAX 200 tokens:
- Vilken fas projektet är i
- Vad som gjordes senast (1 mening)
- Vad som är nästa steg (1-2 punkter)
- Eventuella varningar

Kontext:
$WARM_CONTEXT"

    # Route to cheapest model (haiku/flash) via run.sh
    REFLECT_RESULT=$(echo "$REFLECT_PROMPT" | bash "$RUN_TOOL" --task "reflect" --domain "summarize" --complexity LOW 2>/dev/null) || true

    if [[ -n "$REFLECT_RESULT" ]]; then
      # Extract result from JSON output
      _PY=""
      command -v python3 &>/dev/null && _PY="python3" || _PY="python"
      export _ULTIMA_REFLECT_JSON="$REFLECT_RESULT"
      REFLECTION=$("$_PY" << 'PYEOF' 2>/dev/null
import json, os
raw = os.environ['_ULTIMA_REFLECT_JSON']
try:
    data = json.loads(raw)
    print(data.get('result', raw))
except (json.JSONDecodeError, KeyError):
    print(raw)
PYEOF
      ) || REFLECTION="$REFLECT_RESULT"
      unset _ULTIMA_REFLECT_JSON

      # Identity always included, even in reflect mode
      if [[ -f "$IDENTITY_DIR/SOUL.md" ]]; then
        echo "## Identity — SOUL"
        echo ""
        cat "$IDENTITY_DIR/SOUL.md"
        echo ""
        echo "---"
        echo ""
      fi
      if [[ -f "$IDENTITY_DIR/USER.md" ]]; then
        echo "## Identity — USER"
        echo ""
        cat "$IDENTITY_DIR/USER.md"
        echo ""
        echo "---"
        echo ""
      fi
      echo "# Reflection Brief"
      echo ""
      echo "_Pre-sammanfattad av billig modell — meta-kognition om kontext._"
      echo ""
      echo "$REFLECTION"
      echo ""
      echo "---"
      exit 0
    else
      echo "REFLECT: Fallback to warm tier (run.sh not available or failed)" >&2
    fi
  else
    echo "REFLECT: No warm context or run.sh not found, falling back to warm tier" >&2
  fi
  # Fallback: continue with normal warm output
  TIER="${TIER:-warm}"
fi

# --- Budget mode: fill knapsack up to N tokens ---
if [[ "$BUDGET" -gt 0 ]]; then
  # Resolve Python
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || _PY="python"

  export _ULTIMA_BUDGET="$BUDGET"
  export _ULTIMA_SOUL="$IDENTITY_DIR/SOUL.md"
  export _ULTIMA_USER="$IDENTITY_DIR/USER.md"
  export _ULTIMA_BRIEF="$CONTEXT_DIR/session-brief.md"
  export _ULTIMA_HANDOFF="$CONTEXT_DIR/handoff.md"
  export _ULTIMA_DISTILLED="$CONTEXT_DIR/distilled.md"
  export _ULTIMA_DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"

  "$_PY" << 'PYEOF'
import os

budget = int(os.environ['_ULTIMA_BUDGET'])
# ~3.5 bytes per token for Swedish/English mix
bytes_budget = int(budget * 3.5)

def read_file(path):
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, OSError):
        return None

# Priority-ordered chunks: highest value first (identity always first)
chunks = [
    ("Identity — SOUL", os.environ['_ULTIMA_SOUL']),
    ("Identity — USER", os.environ['_ULTIMA_USER']),
    ("Status", os.environ['_ULTIMA_BRIEF']),
    ("Handoff", os.environ['_ULTIMA_HANDOFF']),
    ("Distilled", os.environ['_ULTIMA_DISTILLED']),
    ("Raw Discoveries", os.environ['_ULTIMA_DISCOVERIES']),
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
        # Try to fit a truncated version
        remaining = bytes_budget - total_used
        if remaining > 200:  # Only include if meaningful
            truncated = content[:remaining]
            # Cut at last newline to avoid broken lines
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
        break  # Budget full

est_tokens = total_used * 10 // 35
print(f"_Budget: {budget} tok requested, ~{est_tokens} tok used ({total_used} bytes)_")
print(f"_Sections: {', '.join(sections_loaded)}_")
PYEOF

  unset _ULTIMA_BUDGET _ULTIMA_SOUL _ULTIMA_USER _ULTIMA_BRIEF _ULTIMA_HANDOFF _ULTIMA_DISTILLED _ULTIMA_DISCOVERIES
  exit 0
fi

# --- Assemble context based on tier ---
emit_section() {
  local title="$1"
  local file="$2"
  if [[ -f "$file" ]]; then
    if [[ "$FORMAT" == "json" ]]; then
      # JSON mode: will be assembled later
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

DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"

# Resolve PROJECT.md (search in priority order, not hardcoded)
PROJECT_MD=""
for _candidate in \
  "$WORKSPACE_ROOT/PROJECT.md" \
  "$ULTIMA_ROOT/../PROJECT.md" \
  "$WORKSPACE_ROOT/.openclaw/workspace/projects/ultima-claw/PROJECT.md"; do
  if [[ -f "$_candidate" ]]; then
    PROJECT_MD="$_candidate"
    break
  fi
done
PROJECT_MD="${PROJECT_MD:-/dev/null}"

if [[ "$FORMAT" == "json" && -n "$PYTHON_CMD" ]]; then
  # --- JSON output mode ---
  BRIEF_FILE="$CONTEXT_DIR/session-brief.md"
  HANDOFF_FILE="$CONTEXT_DIR/handoff.md"
  DISTILLED_FILE="$CONTEXT_DIR/distilled.md"

  export _ULTIMA_TIER="$TIER"
  export _ULTIMA_BRIEF="$BRIEF_FILE"
  export _ULTIMA_HANDOFF="$HANDOFF_FILE"
  export _ULTIMA_DISTILLED="$DISTILLED_FILE"
  export _ULTIMA_DISCOVERIES="$DISCOVERIES"
  export _ULTIMA_PROJECT="$PROJECT_MD"
  export _ULTIMA_SOUL="$IDENTITY_DIR/SOUL.md"
  export _ULTIMA_USER="$IDENTITY_DIR/USER.md"
  export _ULTIMA_AGENTS="$IDENTITY_DIR/AGENTS.md"

  "$PYTHON_CMD" << 'PYEOF'
import json, os

tier = os.environ['_ULTIMA_TIER']

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

# Identity: always included
soul = read_if_exists(os.environ['_ULTIMA_SOUL'])
if soul:
    result['sections']['identity_soul'] = soul
user = read_if_exists(os.environ['_ULTIMA_USER'])
if user:
    result['sections']['identity_user'] = user

# Hot tier: always included
brief = read_if_exists(os.environ['_ULTIMA_BRIEF'])
if brief:
    result['sections']['session_brief'] = brief

# Warm tier: add behavior protocol + handoff + distilled
if tier in ('warm', 'cold'):
    agents = read_if_exists(os.environ['_ULTIMA_AGENTS'])
    if agents:
        result['sections']['behavior_protocol'] = agents
    handoff = read_if_exists(os.environ['_ULTIMA_HANDOFF'])
    if handoff:
        result['sections']['handoff'] = handoff

    distilled = read_if_exists(os.environ['_ULTIMA_DISTILLED'])
    if distilled:
        result['sections']['distilled_discoveries'] = distilled

# Cold tier: add full discoveries + project status
if tier == 'cold':
    project = read_if_exists(os.environ['_ULTIMA_PROJECT'])
    if project:
        result['sections']['project_status'] = project

    discoveries = read_discoveries(os.environ['_ULTIMA_DISCOVERIES'], 0)
    result['sections']['raw_discoveries'] = discoveries

# Token estimate (~3.5 bytes/token for mixed Swedish/English UTF-8)
total_chars = sum(len(str(v)) for v in result['sections'].values())
result['estimated_tokens'] = total_chars * 10 // 35
result['total_bytes'] = total_chars

print(json.dumps(result, indent=2, ensure_ascii=False))
PYEOF
  unset _ULTIMA_TIER _ULTIMA_BRIEF _ULTIMA_HANDOFF _ULTIMA_DISTILLED _ULTIMA_DISCOVERIES _ULTIMA_PROJECT _ULTIMA_SOUL _ULTIMA_USER _ULTIMA_AGENTS
else
  # --- Markdown output mode ---
  echo "# Ultima-Claw Context (tier: $TIER)"
  echo ""
  echo "_Loaded: $(date -u +%Y-%m-%dT%H:%M:%SZ)_"
  echo ""

  # Facet priming FIRST (before SOUL.md) for maximum LLM attention
  if [[ -n "$DOMAIN" && -f "$IDENTITY_DIR/SOUL.md" ]]; then
    _PY_FACET=""
    command -v python3 &>/dev/null && _PY_FACET="python3" || _PY_FACET="python"
    SOUL_W=""
    if command -v cygpath &>/dev/null; then
      SOUL_W=$(cygpath -w "$IDENTITY_DIR/SOUL.md")
    else
      SOUL_W="$IDENTITY_DIR/SOUL.md"
    fi
    export _ULTIMA_SOUL_PATH="$SOUL_W"
    export _ULTIMA_DOMAIN="$DOMAIN"
    FACET_MSG=$("$_PY_FACET" << 'PYEOF'
import os

soul_path = os.environ['_ULTIMA_SOUL_PATH']
domain = os.environ['_ULTIMA_DOMAIN'].lower()

with open(soul_path, encoding='utf-8') as f:
    content = f.read()

# Parse facet table rows: | context | emphasis | dampen |
# Skip header and separator rows explicitly
for line in content.split('\n'):
    if not line.startswith('|'):
        continue
    parts = [p.strip() for p in line.split('|')]
    # Check if this is a separator row (any part contains ---)
    if any('---' in p for p in parts):
        continue
    if len(parts) >= 4:
        ctx = parts[1].lower()
        if ctx in ('kontext', ''):
            continue  # header
        # Exact match or hyphenated prefix (code-review-deep matches code-review)
        if ctx == domain or domain.startswith(ctx + '-'):
            print(f"**AKTIV FACETT ({domain}):** {parts[2]} | Dampa: {parts[3]}")
            break
PYEOF
    ) || true
    unset _ULTIMA_SOUL_PATH _ULTIMA_DOMAIN

    if [[ -n "$FACET_MSG" ]]; then
      echo "$FACET_MSG"
      echo ""
      echo "---"
      echo ""
    fi
  fi

  # Identity: always loaded (SOUL + USER define who you are)
  emit_section "Identity -- SOUL" "$IDENTITY_DIR/SOUL.md"
  emit_section "Identity -- USER" "$IDENTITY_DIR/USER.md"

  # Hot: session brief (always)
  emit_section "Session Brief" "$CONTEXT_DIR/session-brief.md"

  # Warm: add handoff + distilled discoveries + behavior protocol
  if [[ "$TIER" == "warm" || "$TIER" == "cold" ]]; then
    emit_section "Behavior Protocol" "$IDENTITY_DIR/AGENTS.md"
    emit_section "Handoff" "$CONTEXT_DIR/handoff.md"
    emit_section "Distilled Discoveries" "$CONTEXT_DIR/distilled.md"
  fi

  # Cold: add full project status + raw discoveries
  if [[ "$TIER" == "cold" ]]; then
    emit_section "Project Status" "$PROJECT_MD"

    if [[ -f "$DISCOVERIES" ]]; then
      echo "## Raw Discoveries (full)"
      echo ""
      echo '```jsonl'
      cat "$DISCOVERIES"
      echo '```'
      echo ""
    fi
  fi

  # Token estimate based on actual tier loaded
  TOTAL_CHARS=0
  # Identity: always loaded
  for _id_file in "$IDENTITY_DIR/SOUL.md" "$IDENTITY_DIR/USER.md"; do
    [[ -f "$_id_file" ]] && {
      _sz=$(wc -c < "$_id_file" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
  done
  # Hot: always
  [[ -f "$CONTEXT_DIR/session-brief.md" ]] && {
    _sz=$(wc -c < "$CONTEXT_DIR/session-brief.md" | tr -d ' ')
    TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
  }
  # Warm/Cold: add AGENTS.md + handoff + distilled
  if [[ "$TIER" == "warm" || "$TIER" == "cold" ]]; then
    [[ -f "$IDENTITY_DIR/AGENTS.md" ]] && {
      _sz=$(wc -c < "$IDENTITY_DIR/AGENTS.md" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
  fi
  # Warm/Cold: add handoff + distilled
  if [[ "$TIER" == "warm" || "$TIER" == "cold" ]]; then
    [[ -f "$CONTEXT_DIR/handoff.md" ]] && {
      _sz=$(wc -c < "$CONTEXT_DIR/handoff.md" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
    [[ -f "$CONTEXT_DIR/distilled.md" ]] && {
      _sz=$(wc -c < "$CONTEXT_DIR/distilled.md" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
  fi
  # Cold: add PROJECT.md + raw discoveries
  if [[ "$TIER" == "cold" ]]; then
    [[ -f "$PROJECT_MD" && "$PROJECT_MD" != "/dev/null" ]] && {
      _sz=$(wc -c < "$PROJECT_MD" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
    [[ -f "$DISCOVERIES" ]] && {
      _sz=$(wc -c < "$DISCOVERIES" | tr -d ' ')
      TOTAL_CHARS=$(( TOTAL_CHARS + _sz ))
    }
  fi
  # ~3.5 bytes/token for mixed Swedish/English UTF-8
  EST_TOKENS=$(( TOTAL_CHARS * 10 / 35 ))
  echo "_Estimated context: ~${EST_TOKENS} tokens (${TOTAL_CHARS} bytes)_"
fi
