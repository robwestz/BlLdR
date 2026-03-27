#!/usr/bin/env bash
# wave-track.sh — Track wave lifecycle
#
# Usage:
#   wave-track.sh --start                            # Create wave, return ID
#   wave-track.sh --end --session 2026-03-05-001    # Close wave with stats
#   wave-track.sh --list                             # List recent waves
#
# Session files: continuum/sessions/YYYY-MM-DD-NNN.json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SESSIONS_DIR="$MEMORY_ROOT/continuum/sessions"
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

ACTION=""
SESSION_ID=""
ENGINE="claude"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --start)   ACTION="start"; shift ;;
    --end)     ACTION="end"; shift ;;
    --list)    ACTION="list"; shift ;;
    --session) SESSION_ID="$2"; shift 2 ;;
    --engine)  ENGINE="$2"; shift 2 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$SESSIONS_DIR"

case "$ACTION" in
  start)
    TODAY=$(date -u +%Y-%m-%d)
    # Find next sequence number for today
    SEQ=1
    while [[ -f "$SESSIONS_DIR/${TODAY}-$(printf '%03d' $SEQ).json" ]]; do
      SEQ=$((SEQ + 1))
    done
    SESSION_ID="${TODAY}-$(printf '%03d' $SEQ)"

    NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    cat > "$SESSIONS_DIR/${SESSION_ID}.json" << EOF
{
  "id": "$SESSION_ID",
  "started": "$NOW",
  "ended": null,
  "engine": "$ENGINE",
  "wave": "",
  "discoveries_count": 0,
  "commits_count": 0,
  "handoff_created": false
}
EOF
    echo "$SESSION_ID"
    echo "wave-track: started $SESSION_ID" >&2
    ;;

  end)
    if [[ -z "$SESSION_ID" ]]; then
      # Find most recent open session
      SESSION_ID=$(ls -1 "$SESSIONS_DIR"/*.json 2>/dev/null | sort | tail -1 | xargs basename 2>/dev/null | sed 's/.json//' || true)
      if [[ -z "$SESSION_ID" ]]; then
        echo "ERROR: No wave to end. Use --session ID or start one first." >&2
        exit 1
      fi
    fi

    SESSION_FILE="$SESSIONS_DIR/${SESSION_ID}.json"
    if [[ ! -f "$SESSION_FILE" ]]; then
      echo "ERROR: Session file not found: $SESSION_FILE" >&2
      exit 1
    fi

    NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    # Count discoveries written during this session
    DISC_COUNT=0
    if [[ -f "$DISCOVERIES" && -s "$DISCOVERIES" ]]; then
      # Read session start time
      START_TS=$(export _F="$SESSION_FILE"; "$PYTHON_CMD" -c "
import json, os
with open(os.environ['_F'], encoding='utf-8') as f:
    print(json.load(f)['started'])
" 2>/dev/null) || START_TS=""

      if [[ -n "$START_TS" ]]; then
        DISC_COUNT=$(export _D="$DISCOVERIES" _S="$START_TS"; "$PYTHON_CMD" -c "
import json, os
start = os.environ['_S']
count = 0
with open(os.environ['_D'], encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            if d.get('ts', '') >= start:
                count += 1
        except: pass
print(count)
" 2>/dev/null) || DISC_COUNT=0
      fi
    fi

    # Count commits during session
    GIT_ROOT=""
    COMMITS_COUNT=0
    WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"
    if git -C "$WORKSPACE_ROOT" rev-parse --show-toplevel &>/dev/null; then
      GIT_ROOT=$(git -C "$WORKSPACE_ROOT" rev-parse --show-toplevel)
      START_TS=$(export _F="$SESSION_FILE"; "$PYTHON_CMD" -c "
import json, os
with open(os.environ['_F'], encoding='utf-8') as f:
    print(json.load(f)['started'])
" 2>/dev/null) || START_TS=""
      if [[ -n "$START_TS" ]]; then
        COMMITS_COUNT=$(git -C "$GIT_ROOT" log --since="$START_TS" --oneline 2>/dev/null | wc -l | tr -d ' ') || COMMITS_COUNT=0
      fi
    fi

    # Check if handoff was created
    HANDOFF_CREATED=false
    HANDOFF_FILE="$MEMORY_ROOT/context/handoff.md"
    if [[ -f "$HANDOFF_FILE" ]]; then
      # Check if handoff was modified after session start
      START_TS=$(export _F="$SESSION_FILE"; "$PYTHON_CMD" -c "
import json, os
with open(os.environ['_F'], encoding='utf-8') as f:
    print(json.load(f)['started'])
" 2>/dev/null) || START_TS=""
      if [[ -n "$START_TS" ]]; then
        HANDOFF_CREATED=$(export _H="$HANDOFF_FILE" _S="$START_TS"; "$PYTHON_CMD" -c "
import os
from datetime import datetime, timezone
start = os.environ['_S']
mtime = os.path.getmtime(os.environ['_H'])
file_dt = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('true' if file_dt >= start else 'false')
" 2>/dev/null) || HANDOFF_CREATED="false"
      fi
    fi

    # Update session file atomically
    TMPFILE=$(mktemp)
    export _SF="$SESSION_FILE" _NOW="$NOW" _DC="$DISC_COUNT" _CC="$COMMITS_COUNT" _HC="$HANDOFF_CREATED"
    "$PYTHON_CMD" << 'PYEOF' > "$TMPFILE"
import json, os
with open(os.environ['_SF'], encoding='utf-8') as f:
    data = json.load(f)
data['ended'] = os.environ['_NOW']
data['discoveries_count'] = int(os.environ['_DC'])
data['commits_count'] = int(os.environ['_CC'])
data['handoff_created'] = os.environ['_HC'] == 'true'
print(json.dumps(data, indent=2, ensure_ascii=False))
PYEOF
    mv "$TMPFILE" "$SESSION_FILE"
    unset _SF _NOW _DC _CC _HC

    echo "wave-track: ended $SESSION_ID (discoveries=$DISC_COUNT, commits=$COMMITS_COUNT, handoff=$HANDOFF_CREATED)" >&2
    cat "$SESSION_FILE"
    ;;

  list)
    echo "=== Recent Waves ==="
    shopt -s nullglob
    SESSION_FILES=("$SESSIONS_DIR"/*.json)
    shopt -u nullglob
    printf '%s\n' "${SESSION_FILES[@]}" | sort | tail -10 | while read -r f; do
      [[ -z "$f" ]] && continue
      export _F="$f"
      "$PYTHON_CMD" -c "
import json, os
with open(os.environ['_F'], encoding='utf-8') as f:
    d = json.load(f)
status = 'OPEN' if d.get('ended') is None else 'DONE'
disc = d.get('discoveries_count', '?')
print(f\"  {d['id']}  [{status}]  engine={d.get('engine','?')}  discoveries={disc}\")
" 2>/dev/null || true
      unset _F
    done
    ;;

  *)
    echo "ERROR: Specify --start, --end, or --list" >&2
    exit 1
    ;;
esac
