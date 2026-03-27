#!/usr/bin/env bash
set -euo pipefail

# project-registry.sh — Track Buildr workspaces across sessions
#
# Usage:
#   project-registry.sh --register --name NAME --path PATH --category CAT [--origin new|rescue]
#   project-registry.sh --update --name NAME --status STATUS [--wave WAVE] [--hint "..."]
#   project-registry.sh --activate --name NAME
#   project-registry.sh --list [--status STATUS]
#   project-registry.sh --active
#   project-registry.sh --pause --name NAME --reason "..."
#   project-registry.sh --resume --name NAME

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"
PYTHON="$(resolve_python)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY="$MEMORY_ROOT/registry/projects.json"
ACTIVE="$MEMORY_ROOT/registry/active.json"

# For Python on Windows: convert /c/... to C:/... so Python can find files
_py_path() {
  local p="$1"
  if [[ "$p" =~ ^/([a-zA-Z])/ ]]; then
    echo "${BASH_REMATCH[1]^}:/${p:3}"
  else
    echo "$p"
  fi
}
_PY_REG="$(_py_path "$REGISTRY")"
_PY_ACT="$(_py_path "$ACTIVE")"

# Ensure files exist
[[ -f "$REGISTRY" ]] || echo '[]' > "$REGISTRY"
[[ -f "$ACTIVE" ]] || echo '{"active_project": null}' > "$ACTIVE"

ACTION=""
NAME=""
PROJECT_PATH=""
CATEGORY=""
STATUS=""
WAVE=""
HINT=""
REASON=""
ORIGIN="new"
FILTER_STATUS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --register)  ACTION="register"; shift ;;
    --update)    ACTION="update"; shift ;;
    --activate)  ACTION="activate"; shift ;;
    --list)      ACTION="list"; shift ;;
    --active)    ACTION="active"; shift ;;
    --pause)     ACTION="pause"; shift ;;
    --resume)    ACTION="resume"; shift ;;
    --name)      NAME="$2"; shift 2 ;;
    --path)      PROJECT_PATH="$2"; shift 2 ;;
    --category)  CATEGORY="$2"; shift 2 ;;
    --status)    if [[ "$ACTION" == "list" ]]; then FILTER_STATUS="$2"; else STATUS="$2"; fi; shift 2 ;;
    --wave)      WAVE="$2"; shift 2 ;;
    --hint)      HINT="$2"; shift 2 ;;
    --reason)    REASON="$2"; shift 2 ;;
    --origin)    ORIGIN="$2"; shift 2 ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

TODAY="$(date +%Y-%m-%d)"

case "$ACTION" in

  register)
    [[ -z "$NAME" ]] && { echo "ERROR: --name required" >&2; exit 1; }
    [[ -z "$PROJECT_PATH" ]] && { echo "ERROR: --path required" >&2; exit 1; }

    $PYTHON -c "
import json, sys
reg = json.load(open('$_PY_REG'))
# Check duplicate
if any(p['name'] == '$NAME' for p in reg):
    print(f'project-registry: $NAME already registered', file=sys.stderr)
    sys.exit(1)
reg.append({
    'name': '$NAME',
    'path': '$PROJECT_PATH',
    'category': '${CATEGORY:-unknown}',
    'origin': '$ORIGIN',
    'status': 'in_progress',
    'current_wave': '001',
    'created': '$TODAY',
    'last_touched': '$TODAY',
    'paused_reason': None,
    'resume_hint': None
})
json.dump(reg, open('$_PY_REG', 'w'), indent=2, ensure_ascii=False)
print(f'project-registry: registered $NAME ($ORIGIN)')
"
    # Auto-activate
    $PYTHON -c "
import json
a = {'active_project': '$NAME'}
json.dump(a, open('$_PY_ACT', 'w'), indent=2)
"
    ;;

  update)
    [[ -z "$NAME" ]] && { echo "ERROR: --name required" >&2; exit 1; }

    $PYTHON -c "
import json, sys
reg = json.load(open('$_PY_REG'))
found = False
for p in reg:
    if p['name'] == '$NAME':
        found = True
        p['last_touched'] = '$TODAY'
        if '$STATUS': p['status'] = '$STATUS'
        if '$WAVE': p['current_wave'] = '$WAVE'
        if '$HINT': p['resume_hint'] = '$HINT'
        break
if not found:
    print(f'project-registry: $NAME not found', file=sys.stderr)
    sys.exit(1)
json.dump(reg, open('$_PY_REG', 'w'), indent=2, ensure_ascii=False)
print(f'project-registry: updated $NAME')
"
    ;;

  activate)
    [[ -z "$NAME" ]] && { echo "ERROR: --name required" >&2; exit 1; }

    $PYTHON -c "
import json
a = {'active_project': '$NAME'}
json.dump(a, open('$_PY_ACT', 'w'), indent=2)
print(f'project-registry: $NAME is now active')
"
    ;;

  active)
    $PYTHON -c "
import json
a = json.load(open('$_PY_ACT'))
reg = json.load(open('$_PY_REG'))
name = a.get('active_project')
if not name:
    print('No active project')
else:
    proj = next((p for p in reg if p['name'] == name), None)
    if proj:
        print(f\"Active: {proj['name']} ({proj['status']})\")
        print(f\"  Path: {proj['path']}\")
        print(f\"  Category: {proj['category']}  Origin: {proj['origin']}\")
        print(f\"  Wave: {proj['current_wave']}  Last: {proj['last_touched']}\")
        if proj.get('resume_hint'):
            print(f\"  Resume: {proj['resume_hint']}\")
        if proj.get('paused_reason'):
            print(f\"  Paused: {proj['paused_reason']}\")
    else:
        print(f'Active project {name} not in registry')
"
    ;;

  list)
    $PYTHON -c "
import json
reg = json.load(open('$_PY_REG'))
filt = '$FILTER_STATUS'
if filt:
    reg = [p for p in reg if p['status'] == filt]
if not reg:
    print('No projects' + (f' with status={filt}' if filt else ''))
else:
    for p in reg:
        flag = '>' if p['status'] == 'in_progress' else ' '
        origin_tag = '[R]' if p['origin'] == 'rescue' else '   '
        print(f\"{flag} {origin_tag} {p['name']:30s} {p['status']:15s} wave {p['current_wave']}  ({p['last_touched']})\")
        if p.get('resume_hint'):
            print(f\"        {p['resume_hint']}\")
"
    ;;

  pause)
    [[ -z "$NAME" ]] && { echo "ERROR: --name required" >&2; exit 1; }

    $PYTHON -c "
import json, sys
reg = json.load(open('$_PY_REG'))
for p in reg:
    if p['name'] == '$NAME':
        p['status'] = 'paused'
        p['paused_reason'] = '$REASON' or 'No reason given'
        p['last_touched'] = '$TODAY'
        break
json.dump(reg, open('$_PY_REG', 'w'), indent=2, ensure_ascii=False)
print(f'project-registry: $NAME paused')
"
    ;;

  resume)
    [[ -z "$NAME" ]] && { echo "ERROR: --name required" >&2; exit 1; }

    $PYTHON -c "
import json
reg = json.load(open('$_PY_REG'))
for p in reg:
    if p['name'] == '$NAME':
        p['status'] = 'in_progress'
        p['paused_reason'] = None
        p['last_touched'] = '$TODAY'
        break
json.dump(reg, open('$_PY_REG', 'w'), indent=2, ensure_ascii=False)
# Also set as active
a = {'active_project': '$NAME'}
json.dump(a, open('$_PY_ACT', 'w'), indent=2)
print(f'project-registry: $NAME resumed and activated')
"
    ;;

  *)
    echo "Usage: project-registry.sh --register|--update|--activate|--list|--active|--pause|--resume" >&2
    exit 1
    ;;
esac
