#!/usr/bin/env bash
# inject-context.sh — Read discoveries and inject summary into CLAUDE.md (and future GEMINI.md)
#
# Usage:
#   inject-context.sh [--target CLAUDE.md] [--max 30] [--dry-run]
#   inject-context.sh --tier hot          # Inject only session brief (~200 tokens)
#   inject-context.sh --tier warm         # Inject distilled discoveries (~1K tokens)
#   inject-context.sh --tier cold         # Inject all raw discoveries (legacy behavior)
#
# Reads .ultima/continuum/discoveries.jsonl, formats the latest N entries,
# and injects them between marker comments in the target file.
#
# Tiers (context engineering):
#   hot  — Last 3 discoveries only. Minimal footprint.
#   warm — Distilled summaries from context/distilled.md. Default.
#   cold — All raw discoveries (legacy --max behavior).
#
# Markers in target file:
#   <!-- ULTIMA-INJECT-START -->
#   (auto-generated content here)
#   <!-- ULTIMA-INJECT-END -->
#
# If markers don't exist, appends a new section before "## Referenser" or at end.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$ULTIMA_ROOT/.." && pwd)"
DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"
CONTEXT_DIR="$ULTIMA_ROOT/context"

# Defaults
TARGET="$WORKSPACE_ROOT/CLAUDE.md"
MAX_ENTRIES=30
DRY_RUN=false
TIER=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)  TARGET="$2";      shift 2 ;;
    --max)     MAX_ENTRIES="$2";  shift 2 ;;
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
DEFAULTS_CONFIG="$ULTIMA_ROOT/config/defaults.json"
PYTHON_CMD=""
command -v python3 &>/dev/null && PYTHON_CMD="python3" || { command -v python &>/dev/null && PYTHON_CMD="python"; }

MARKER_START="<!-- MEMORY-INJECT-START -->"
MARKER_END="<!-- MEMORY-INJECT-END -->"
if [[ -n "$PYTHON_CMD" && -f "$DEFAULTS_CONFIG" ]]; then
  _cfg="$DEFAULTS_CONFIG"
  [[ "$(command -v cygpath 2>/dev/null)" ]] && _cfg=$(cygpath -w "$_cfg")
  export _ULTIMA_CFG="$_cfg"
  MARKER_START=$("$PYTHON_CMD" << 'PYEOF'
import json, os
with open(os.environ['_ULTIMA_CFG'], encoding='utf-8') as f:
    print(json.load(f).get('context_injection',{}).get('marker_start','<!-- MEMORY-INJECT-START -->'))
PYEOF
  ) || true
  MARKER_END=$("$PYTHON_CMD" << 'PYEOF'
import json, os
with open(os.environ['_ULTIMA_CFG'], encoding='utf-8') as f:
    print(json.load(f).get('context_injection',{}).get('marker_end','<!-- MEMORY-INJECT-END -->'))
PYEOF
  ) || true
  unset _ULTIMA_CFG
fi

# --- Build formatted content based on tier ---
FORMATTED=""

if [[ "$TIER" == "warm" ]]; then
  # Warm tier: use distilled.md (pre-compressed topic summaries)
  DISTILLED="$CONTEXT_DIR/distilled.md"
  if [[ ! -f "$DISTILLED" ]]; then
    # Generate distilled.md if missing
    if [[ -x "$SCRIPT_DIR/distill-discoveries.sh" ]]; then
      "$SCRIPT_DIR/distill-discoveries.sh" > "$DISTILLED" 2>/dev/null || true
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
    # Extract fields using basic text processing (no jq dependency)
    ts=$(echo "$line" | sed 's/.*"ts":"\([^"]*\)".*/\1/' | cut -c1-10)
    session=$(echo "$line" | sed 's/.*"session":"\([^"]*\)".*/\1/')
    engine=$(echo "$line" | sed 's/.*"engine":"\([^"]*\)".*/\1/')
    topic=$(echo "$line" | sed 's/.*"topic":"\([^"]*\)".*/\1/')
    content=$(echo "$line" | sed 's/.*"content":"\([^"]*\)".*/\1/')

    # Handle entries without engine field (legacy format)
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
  # Replace content between markers
  # Create temp file
  TMPFILE=$(mktemp)
  IN_BLOCK=false
  while IFS= read -r line; do
    if [[ "$line" == *"$MARKER_START"* ]]; then
      echo "$INJECT_BLOCK" >> "$TMPFILE"
      IN_BLOCK=true
    elif [[ "$line" == *"$MARKER_END"* ]]; then
      IN_BLOCK=false
      # Already written as part of INJECT_BLOCK
    elif ! $IN_BLOCK; then
      echo "$line" >> "$TMPFILE"
    fi
  done < "$TARGET"
  mv "$TMPFILE" "$TARGET"
  echo "OK: Injected ${MAX_ENTRIES} discoveries (replaced existing block) in $TARGET" >&2
else
  # No markers — insert before "## Referenser" or append
  if grep -q "^## Referenser" "$TARGET"; then
    TMPFILE=$(mktemp)
    while IFS= read -r line; do
      if [[ "$line" == "## Referenser" ]]; then
        echo "" >> "$TMPFILE"
        echo "## Continuum — Senaste discoveries" >> "$TMPFILE"
        echo "$INJECT_BLOCK" >> "$TMPFILE"
        echo "" >> "$TMPFILE"
      fi
      echo "$line" >> "$TMPFILE"
    done < "$TARGET"
    mv "$TMPFILE" "$TARGET"
  else
    # Append at end
    echo "" >> "$TARGET"
    echo "## Continuum — Senaste discoveries" >> "$TARGET"
    echo "$INJECT_BLOCK" >> "$TARGET"
  fi
  echo "OK: Injected discoveries (new section) in $TARGET" >&2
fi
