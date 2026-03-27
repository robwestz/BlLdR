#!/usr/bin/env bash
# session-handoff.sh — Generate session handoff contract
#
# Creates a compact "what happened + what's next" document at session end.
# Follows the OpenClaw AGENT_HANDOFF.md pattern: treat the next session
# as a competent colleague, give them exactly what they need.
#
# Usage:
#   session-handoff.sh --session opus-5 --summary "Built context tiers"
#   session-handoff.sh --session opus-5 --summary "..." --next "Implement distillation"
#   session-handoff.sh --session opus-5 --summary "..." --files "tools/x.sh,tools/y.sh"
#
# Output: Writes to .ultima/context/handoff.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$ULTIMA_ROOT/.." && pwd)"
CONTEXT_DIR="$ULTIMA_ROOT/context"
DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"
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

export _ULTIMA_SESSION="$SESSION_ID"
export _ULTIMA_SUMMARY="$SUMMARY"
export _ULTIMA_NEXT="$NEXT_STEPS"
export _ULTIMA_FILES="$FILES_CHANGED"
export _ULTIMA_DISC="$DISCOVERIES_W"

"$PYTHON_CMD" << 'PYEOF' > "$HANDOFF_FILE"
import json, os
from datetime import datetime, timezone

session = os.environ['_ULTIMA_SESSION']
summary = os.environ['_ULTIMA_SUMMARY']
next_steps = os.environ.get('_ULTIMA_NEXT', '')
files_changed = os.environ.get('_ULTIMA_FILES', '')
disc_path = os.environ['_ULTIMA_DISC']

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

print(f"# Session Handoff: {session}")
print(f"> Genererad: {now}")
print()
print("## Sammanfattning")
print(summary)
print()

if session_discoveries:
    print("## Discoveries denna session")
    for d in session_discoveries:
        topic = d.get('topic', '?')
        content = d.get('content', '')
        if len(content) > 150:
            content = content[:147] + "..."
        print(f"- **{topic}**: {content}")
    print()

if files_changed:
    print("## Ändrade filer")
    for f in files_changed.split(','):
        f = f.strip()
        if f:
            print(f"- `{f}`")
    print()

if next_steps:
    print("## Nästa steg")
    for step in next_steps.split(';'):
        step = step.strip()
        if step:
            print(f"- {step}")
    print()
else:
    print("## Nästa steg")
    print("- (Ej specificerat — kolla PROJECT.md)")
    print()

print("## Kontext")
print(f"- Totalt discoveries: {len(all_discoveries)}")
print(f"- Denna session: {len(session_discoveries)} discoveries")
print(f"- Session ID: {session}")
print()
print("---")
print(f"_Nästa session: börja med `context-load.sh --tier warm` för att ladda denna handoff._")
PYEOF

unset _ULTIMA_SESSION _ULTIMA_SUMMARY _ULTIMA_NEXT _ULTIMA_FILES _ULTIMA_DISC

echo "HANDOFF: Written to $HANDOFF_FILE" >&2
