#!/usr/bin/env bash
# memory-inject.sh — Read discoveries and inject summary into MEMORY.md
#
# Usage:
#   memory-inject.sh [--target MEMORY.md] [--max 30] [--dry-run]
#   memory-inject.sh --tier hot          # Inject only wave brief (~200 tokens)
#   memory-inject.sh --tier warm         # Inject distilled discoveries (~1K tokens)
#   memory-inject.sh --tier cold         # Inject all raw discoveries (legacy behavior)
#
# Reads memory-system/continuum/discoveries.jsonl, formats the latest N entries,
# and injects them between marker comments in the target file.
#
# Tiers (context engineering):
#   hot  — Last 3 discoveries only. Minimal footprint.
#   warm — Distilled summaries from context/distilled.md. Default.
#   cold — All raw discoveries (legacy --max behavior).
#
# Markers in target file:
#   <!-- BUILDR-INJECT-START -->
#   (auto-generated content here)
#   <!-- BUILDR-INJECT-END -->
#
# If markers don't exist, appends a new section before "## How to Use This Memory" or at end.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"
DISCOVERIES="$MEMORY_ROOT/continuum/discoveries.jsonl"
CONTEXT_DIR="$MEMORY_ROOT/context"

# Defaults
TARGET="$MEMORY_ROOT/../MEMORY.md"
MAX_ENTRIES=30
DRY_RUN=false
TIER=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)  TARGET="$2";      shift 2 ;;
    --max)     MAX_ENTRIES="$2"; shift 2 ;;
    --tier)    TIER="$2";        shift 2 ;;
    --dry-run) DRY_RUN=true;     shift ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# Tier overrides max_entries
case "$TIER" in
  hot)  MAX_ENTRIES=3 ;;
  warm) MAX_ENTRIES=0 ;;  # Special: use distilled.md instead of raw entries
  cold) ;;                # Use --max or default 30
  "")   ;;                # No tier specified, use legacy behavior
  *)
    echo "ERROR: Invalid tier '$TIER' (use: hot, warm, cold)" >&2
    exit 1
    ;;
esac

# Check target exists
if [[ ! -f "$TARGET" ]]; then
  echo "ERROR: Target file not found: $TARGET" >&2
  exit 1
fi

# Read markers from config (with fallback defaults)
DEFAULTS_CONFIG="$MEMORY_ROOT/config/defaults.json"
PYTHON_CMD=""
command -v python3 &>/dev/null && PYTHON_CMD="python3" || { command -v python &>/dev/null && PYTHON_CMD="python"; }

MARKER_START="<!-- BUILDR-INJECT-START -->"
MARKER_END="<!-- BUILDR-INJECT-END -->"
if [[ -n "$PYTHON_CMD" && -f "$DEFAULTS_CONFIG" ]]; then
  _cfg="$DEFAULTS_CONFIG"
  [[ "$(command -v cygpath 2>/dev/null)" ]] && _cfg=$(cygpath -w "$_cfg")
  export _BUILDR_CFG="$_cfg"
  MARKER_START=$("$PYTHON_CMD" << 'PYEOF'
import json, os
with open(os.environ['_BUILDR_CFG'], encoding='utf-8') as f:
    print(json.load(f).get('context_injection',{}).get('marker_start','<!-- BUILDR-INJECT-START -->'))
PYEOF
  ) || true
  MARKER_END=$("$PYTHON_CMD" << 'PYEOF'
import json, os
with open(os.environ['_BUILDR_CFG'], encoding='utf-8') as f:
    print(json.load(f).get('context_injection',{}).get('marker_end','<!-- BUILDR-INJECT-END -->'))
PYEOF
  ) || true
  unset _BUILDR_CFG
fi

# --- Build formatted content based on tier ---
FORMATTED=""

if [[ "$TIER" == "warm" ]]; then
  # Warm tier: use distilled.md (pre-compressed topic summaries)
  DISTILLED="$CONTEXT_DIR/distilled.md"
  if [[ ! -f "$DISTILLED" ]]; then
    if [[ -x "$SCRIPT_DIR/discovery-distill.sh" ]]; then
      "$SCRIPT_DIR/discovery-distill.sh" > "$DISTILLED" 2>/dev/null || true
    fi
  fi
  if [[ -f "$DISTILLED" ]]; then
    FORMATTED=$(cat "$DISTILLED")
  fi
else
  # Hot or Cold tier: read raw discoveries (latest N)
  if [[ ! -f "$DISCOVERIES" ]]; then
    echo "ERROR: No discoveries file at $DISCOVERIES" >&2
    exit 1
  fi

  while IFS= read -r line; do
    ts=$(echo "$line" | sed 's/.*"ts":"\([^"]*\)".*/\1/' | cut -c1-10)
    session=$(echo "$line" | sed 's/.*"session":"\([^"]*\)".*/\1/')
    engine=$(echo "$line" | sed 's/.*"engine":"\([^"]*\)".*/\1/')
    topic=$(echo "$line" | sed 's/.*"topic":"\([^"]*\)".*/\1/')
    content=$(echo "$line" | sed 's/.*"content":"\([^"]*\)".*/\1/')

    if [[ "$engine" == "$line" ]]; then
      engine="unknown"
    fi

    FORMATTED="${FORMATTED}- ${ts} [${session}/${engine}] ${topic}: ${content}"$'\n'
  done < <(tail -n "$MAX_ENTRIES" "$DISCOVERIES")
fi

if [[ -z "$FORMATTED" ]]; then
  echo "No discoveries to inject." >&2
  exit 0
fi

# Build injection block
INJECT_BLOCK="${MARKER_START}
${FORMATTED}${MARKER_END}"

if $DRY_RUN; then
  echo "=== DRY RUN: Would inject into $TARGET ==="
  echo "$INJECT_BLOCK"
  exit 0
fi

# Check if markers exist in target
if grep -q "$MARKER_START" "$TARGET" && grep -q "$MARKER_END" "$TARGET"; then
  TMPFILE=$(mktemp)
  IN_BLOCK=false
  while IFS= read -r line; do
    if [[ "$line" == *"$MARKER_START"* ]]; then
      echo "$INJECT_BLOCK" >> "$TMPFILE"
      IN_BLOCK=true
    elif [[ "$line" == *"$MARKER_END"* ]]; then
      IN_BLOCK=false
    elif ! $IN_BLOCK; then
      echo "$line" >> "$TMPFILE"
    fi
  done < "$TARGET"
  mv "$TMPFILE" "$TARGET"
  echo "OK: Injected discoveries (replaced existing block) in $TARGET" >&2
else
  if grep -q "^## How to Use This Memory" "$TARGET"; then
    TMPFILE=$(mktemp)
    while IFS= read -r line; do
      if [[ "$line" == "## How to Use This Memory" ]]; then
        echo "" >> "$TMPFILE"
        echo "## Recent Discoveries (auto-injected)" >> "$TMPFILE"
        echo "$INJECT_BLOCK" >> "$TMPFILE"
        echo "" >> "$TMPFILE"
      fi
      echo "$line" >> "$TMPFILE"
    done < "$TARGET"
    mv "$TMPFILE" "$TARGET"
  else
    echo "" >> "$TARGET"
    echo "## Recent Discoveries (auto-injected)" >> "$TARGET"
    echo "$INJECT_BLOCK" >> "$TARGET"
  fi
  echo "OK: Injected discoveries (new section) in $TARGET" >&2
fi
