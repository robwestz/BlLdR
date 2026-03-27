#!/usr/bin/env bash
set -euo pipefail

# vault-select.sh — Shell wrapper for vault_selector.select_for_wave()
#
# Usage:
#   vault-select.sh --intent "booking calendar" --tier C [--category booking] [--stack nextjs]
#   vault-select.sh --wave waves/002-calendar.md
#
# Output: JSON with skills, constraints, routines, memories arrays

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"
PYTHON="$(resolve_python)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"

INTENT=""
TIER="C"
CATEGORY=""
STACK=""
WAVE_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --intent)   INTENT="$2"; shift 2 ;;
    --tier)     TIER="$2"; shift 2 ;;
    --category) CATEGORY="$2"; shift 2 ;;
    --stack)    STACK="$2"; shift 2 ;;
    --wave)     WAVE_FILE="$2"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

# If --wave provided, extract intent and tier from wave file
if [[ -n "$WAVE_FILE" && -f "$WAVE_FILE" ]]; then
  INTENT=$(grep -i "^## Intent" "$WAVE_FILE" -A 2 | tail -1 | sed 's/^[- ]*//' || echo "")
  TIER=$(grep -i "^tier:" "$WAVE_FILE" | head -1 | awk '{print $2}' || echo "C")
fi

[[ -z "$INTENT" ]] && { echo "ERROR: --intent required (or --wave with Intent section)" >&2; exit 1; }

# Convert repo root for Python
_py_path() {
  local p="$1"
  if [[ "$p" =~ ^/([a-zA-Z])/ ]]; then
    echo "${BASH_REMATCH[1]^}:/${p:3}"
  else
    echo "$p"
  fi
}

PY_REPO="$(_py_path "$REPO_ROOT")"

$PYTHON -c "
import sys, json
sys.path.insert(0, '$PY_REPO')
from engines.vault_selector import select_for_wave

result = select_for_wave(
    intent='$INTENT',
    tier='$TIER',
    category='$CATEGORY' or None,
    stack='$STACK' or None,
)
print(json.dumps(result, indent=2, ensure_ascii=False))
"
