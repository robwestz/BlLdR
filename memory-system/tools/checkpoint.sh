#!/usr/bin/env bash
# checkpoint.sh — Snapshot current state to continuum/checkpoints/
#
# Usage:
#   checkpoint.sh                         # Create checkpoint with auto-slug
#   checkpoint.sh --slug my-milestone     # Custom slug
#   checkpoint.sh --auto                  # Only checkpoint if 10+ new discoveries since last
#
# Creates: continuum/checkpoints/YYYY-MM-DD-slug/
#   - discoveries.jsonl, wave-brief.md, distilled.md, handoff.md
#   - manifest.json (metadata)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CHECKPOINTS_DIR="$MEMORY_ROOT/continuum/checkpoints"
DISCOVERIES="$MEMORY_ROOT/continuum/discoveries.jsonl"

# --- Resolve Python ---
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
  PYTHON_CMD="python"
else
  echo "ERROR: Python required" >&2
  exit 1
fi

SLUG=""
AUTO_MODE=false
THRESHOLD=10

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug)      SLUG="$2"; shift 2 ;;
    --auto)      AUTO_MODE=true; shift ;;
    --threshold) THRESHOLD="$2"; shift 2 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$CHECKPOINTS_DIR"

# --- Count current discoveries ---
DISC_COUNT=0
if [[ -f "$DISCOVERIES" && -s "$DISCOVERIES" ]]; then
  DISC_COUNT=$(grep -c . "$DISCOVERIES" 2>/dev/null || echo 0)
fi

# --- Auto mode: check if checkpoint needed ---
if [[ "$AUTO_MODE" == true ]]; then
  LAST_CP_COUNT=0
  LATEST_CP=$(ls -1d "$CHECKPOINTS_DIR"/*/manifest.json 2>/dev/null | sort | tail -1 || true)
  if [[ -n "$LATEST_CP" ]]; then
    LAST_CP_COUNT=$(export _F="$LATEST_CP"; "$PYTHON_CMD" -c "
import json, os
with open(os.environ['_F'], encoding='utf-8') as f:
    print(json.load(f).get('discovery_count', 0))
" 2>/dev/null) || LAST_CP_COUNT=0
  fi

  NEW_SINCE=$((DISC_COUNT - LAST_CP_COUNT))
  if [[ "$NEW_SINCE" -lt "$THRESHOLD" ]]; then
    echo "checkpoint: skip (only $NEW_SINCE new discoveries, need $THRESHOLD)" >&2
    exit 0
  fi
  echo "checkpoint: $NEW_SINCE new discoveries since last checkpoint, creating..." >&2
fi

# --- Generate slug ---
TODAY=$(date -u +%Y-%m-%d)
if [[ -z "$SLUG" ]]; then
  SLUG="checkpoint"
fi
# Ensure unique directory
CP_DIR="$CHECKPOINTS_DIR/${TODAY}-${SLUG}"
SEQ=1
while [[ -d "$CP_DIR" ]]; do
  CP_DIR="$CHECKPOINTS_DIR/${TODAY}-${SLUG}-${SEQ}"
  SEQ=$((SEQ + 1))
done

mkdir -p "$CP_DIR"

# --- Copy state files ---
COPIED=()

if [[ -f "$DISCOVERIES" ]]; then
  cp "$DISCOVERIES" "$CP_DIR/discoveries.jsonl"
  COPIED+=("discoveries.jsonl")
fi

for ctx_file in wave-brief.md distilled.md handoff.md; do
  SRC="$MEMORY_ROOT/context/$ctx_file"
  if [[ -f "$SRC" ]]; then
    cp "$SRC" "$CP_DIR/$ctx_file"
    COPIED+=("$ctx_file")
  fi
done

# --- Get git HEAD ---
GIT_HEAD=""
WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"
if git -C "$WORKSPACE_ROOT" rev-parse HEAD &>/dev/null; then
  GIT_HEAD=$(git -C "$WORKSPACE_ROOT" rev-parse --short HEAD 2>/dev/null || echo "")
fi

# --- Write manifest ---
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$CP_DIR/manifest.json" << EOF
{
  "timestamp": "$NOW",
  "slug": "$SLUG",
  "discovery_count": $DISC_COUNT,
  "git_head": "$GIT_HEAD",
  "trigger": "$(if [[ "$AUTO_MODE" == true ]]; then echo "auto"; else echo "manual"; fi)",
  "files": $(printf '%s\n' "${COPIED[@]}" | "$PYTHON_CMD" -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))")
}
EOF

echo "checkpoint: created $CP_DIR ($DISC_COUNT discoveries, git=$GIT_HEAD)" >&2
echo "$CP_DIR"
