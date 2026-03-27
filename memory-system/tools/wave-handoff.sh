#!/usr/bin/env bash
# wave-handoff.sh — Generate wave handoff contract
#
# Creates a compact "what happened + what's next" document at wave end.
# Treat the next wave as a competent colleague and give it exactly what it needs.
#
# Usage:
#   wave-handoff.sh --session opus-5 --summary "Built context tiers"
#   wave-handoff.sh --session opus-5 --summary "..." --next "Implement distillation"
#   wave-handoff.sh --session opus-5 --summary "..." --files "tools/x.sh,tools/y.sh"
#
# Output: Writes to memory-system/context/handoff.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"
CONTEXT_DIR="$MEMORY_ROOT/context"
DISCOVERIES="$MEMORY_ROOT/continuum/discoveries.jsonl"
HANDOFF_FILE="$CONTEXT_DIR/handoff.md"

# --- Parse args ---
SESSION_ID=""
SUMMARY=""
NEXT_STEPS=""
FILES_CHANGED=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)  SESSION_ID="$2";    shift 2 ;;
    --summary)  SUMMARY="$2";       shift 2 ;;
    --next)     NEXT_STEPS="$2";    shift 2 ;;
    --files)    FILES_CHANGED="$2"; shift 2 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$SESSION_ID" ]]; then
  echo "ERROR: --session required" >&2
  exit 1
fi

if [[ -z "$SUMMARY" ]]; then
  echo "ERROR: --summary required" >&2
  exit 1
fi

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

# Windows path conversion
winpath() {
  if command -v cygpath &>/dev/null; then
    cygpath -w "$1"
  else
    echo "$1"
  fi
}

DISCOVERIES_W=$(winpath "$DISCOVERIES")

mkdir -p "$CONTEXT_DIR"

export _BUILDR_SESSION="$SESSION_ID"
export _BUILDR_SUMMARY="$SUMMARY"
export _BUILDR_NEXT="$NEXT_STEPS"
export _BUILDR_FILES="$FILES_CHANGED"
export _BUILDR_DISC="$DISCOVERIES_W"

"$PYTHON_CMD" << 'PYEOF' > "$HANDOFF_FILE"
import json, os
from datetime import datetime, timezone

session = os.environ['_BUILDR_SESSION']
summary = os.environ['_BUILDR_SUMMARY']
next_steps = os.environ.get('_BUILDR_NEXT', '')
files_changed = os.environ.get('_BUILDR_FILES', '')
disc_path = os.environ['_BUILDR_DISC']

# Read session's discoveries (matching session ID)
session_discoveries = []
all_discoveries = []
try:
    with open(disc_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                all_discoveries.append(entry)
                if entry.get('session', '') == session:
                    session_discoveries.append(entry)
            except json.JSONDecodeError:
                continue
except FileNotFoundError:
    pass

now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

print(f"# Wave Handoff: {session}")
print(f"> Generated: {now}")
print()
print("## Summary")
print(summary)
print()

if session_discoveries:
    print("## Discoveries This Wave")
    for d in session_discoveries:
        topic = d.get('topic', '?')
        content = d.get('content', '')
        if len(content) > 150:
            content = content[:147] + "..."
        print(f"- **{topic}**: {content}")
    print()

if files_changed:
    print("## Changed Files")
    for f in files_changed.split(','):
        f = f.strip()
        if f:
            print(f"- `{f}`")
    print()

if next_steps:
    print("## Next Steps")
    for step in next_steps.split(';'):
        step = step.strip()
        if step:
            print(f"- {step}")
    print()
else:
    print("## Next Steps")
    print("- (Not specified — check PROJECT.md)")
    print()

print("## Context")
print(f"- Total discoveries: {len(all_discoveries)}")
print(f"- This wave: {len(session_discoveries)} discoveries")
print(f"- Session ID: {session}")
print()
print("---")
print("_Next wave: run `context-load.sh --tier warm` to load this handoff._")
PYEOF

unset _BUILDR_SESSION _BUILDR_SUMMARY _BUILDR_NEXT _BUILDR_FILES _BUILDR_DISC

echo "HANDOFF: Written to $HANDOFF_FILE" >&2
