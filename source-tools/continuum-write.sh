#!/usr/bin/env bash
# continuum-write.sh — Append a discovery to .ultima/continuum/discoveries.jsonl
#
# Usage:
#   continuum-write.sh --session SESSION --engine ENGINE --topic TOPIC --content "CONTENT" [--type TYPE] [--artifacts "file1,file2"] [--project PROJECT]
#
# Types: fact, preference, insight (default), event, decision, error
#
# Example:
#   continuum-write.sh --session opus-2 --engine claude --topic model-router --type decision --content "Domain match should precede complexity match" --artifacts ".ultima/config/routing.json"
#
# Output: The appended JSON line (to stdout), and writes to discoveries.jsonl

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"

# Defaults
SESSION=""
ENGINE=""
TOPIC=""
CONTENT=""
TYPE="insight"
ARTIFACTS=""
PROJECT="ultima-claw"

# Valid discovery types
VALID_TYPES="fact preference insight event decision error"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)  SESSION="$2";  shift 2 ;;
    --engine)   ENGINE="$2";   shift 2 ;;
    --topic)    TOPIC="$2";    shift 2 ;;
    --content)  CONTENT="$2";  shift 2 ;;
    --type)     TYPE="$2";     shift 2 ;;
    --artifacts) ARTIFACTS="$2"; shift 2 ;;
    --project)  PROJECT="$2";  shift 2 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      echo "Usage: continuum-write.sh --session SESSION --engine ENGINE --topic TOPIC --content \"CONTENT\" [--type TYPE] [--artifacts \"f1,f2\"] [--project PROJECT]" >&2
      exit 1
      ;;
  esac
done

# Validate required
if [[ -z "$SESSION" || -z "$ENGINE" || -z "$TOPIC" || -z "$CONTENT" ]]; then
  echo "ERROR: --session, --engine, --topic, and --content are required" >&2
  exit 1
fi

# Normalize topic: lowercase, spaces→hyphens, strip non-alphanumeric except hyphen
TOPIC=$(printf '%s' "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | sed 's/--*/-/g; s/^-//; s/-$//')

# --- Type validation ---
TYPE_VALID=false
for _t in $VALID_TYPES; do
  [[ "$TYPE" == "$_t" ]] && TYPE_VALID=true
done
if [[ "$TYPE_VALID" != true ]]; then
  echo "ERROR: --type must be one of: $VALID_TYPES (got: $TYPE)" >&2
  exit 1
fi

# --- Engine validation (config-driven) ---
# Read whitelist from defaults.json, fallback to hardcoded if config unavailable
ENGINE_VALID=false
if [[ -f "$ULTIMA_ROOT/config/defaults.json" ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -n "$_PY" ]]; then
    export _ULTIMA_DEFAULTS="$ULTIMA_ROOT/config/defaults.json"
    WHITELIST=$("$_PY" -c "
import json, os
try:
    with open(os.environ['_ULTIMA_DEFAULTS'], encoding='utf-8') as f:
        cfg = json.load(f)
    wl = cfg.get('security', {}).get('engine_whitelist', ['claude','gemini','codex'])
    print(' '.join(wl))
except Exception:
    print('claude gemini codex')
" 2>/dev/null) || WHITELIST="claude gemini codex"
    unset _ULTIMA_DEFAULTS
  else
    WHITELIST="claude gemini codex"
  fi
else
  WHITELIST="claude gemini codex"
fi
for _e in $WHITELIST; do
  [[ "$ENGINE" == "$_e" ]] && ENGINE_VALID=true
done
if [[ "$ENGINE_VALID" != true ]]; then
  echo "ERROR: --engine must be one of: $WHITELIST (got: $ENGINE)" >&2
  exit 1
fi

# --- Secret guardrails ---
# Check content (and artifacts) against secret patterns before writing
_check_secrets() {
  local text="$1"
  local patterns=(
    '(api[_-]?key|secret[_-]?key)[[:space:]]*[=:][[:space:]]*[^[:space:]]{8,}'
    '(password|passwd|pwd)[[:space:]]*[=:][[:space:]]*[^[:space:]]{8,}'
    'sk-[a-zA-Z0-9]{20,}'
    'ghp_[a-zA-Z0-9]{36,}'
    '(bearer|token)[[:space:]]+[a-zA-Z0-9_\.\-]{20,}'
  )
  for pat in "${patterns[@]}"; do
    if echo "$text" | grep -iEq "$pat"; then
      return 0  # secret found
    fi
  done
  return 1  # clean
}

# Read deny_write_if_secret_like from config (default: true)
DENY_SECRETS=true
if [[ -f "$ULTIMA_ROOT/config/defaults.json" ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -n "$_PY" ]]; then
    export _ULTIMA_DEFAULTS="$ULTIMA_ROOT/config/defaults.json"
    _DENY_CFG=$("$_PY" -c "
import json, os
try:
    with open(os.environ['_ULTIMA_DEFAULTS'], encoding='utf-8') as f:
        cfg = json.load(f)
    print('true' if cfg.get('security', {}).get('deny_write_if_secret_like', True) else 'false')
except Exception:
    print('true')
" 2>/dev/null) || _DENY_CFG="true"
    unset _ULTIMA_DEFAULTS
    DENY_SECRETS="$_DENY_CFG"
  fi
fi

if [[ "$DENY_SECRETS" == "true" ]]; then
  if _check_secrets "$CONTENT" || _check_secrets "$ARTIFACTS"; then
    echo "ERROR: Content appears to contain secrets (API keys, passwords, tokens)." >&2
    echo "REJECTED: Discovery NOT written. Remove secrets and try again." >&2
    exit 2
  fi
fi

# JSON-escape a string: backslashes, quotes, tabs, newlines
json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | tr '\n' ' '
}

# Generate timestamp
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Escape ALL string fields
ESCAPED_SESSION=$(json_escape "$SESSION")
ESCAPED_TOPIC=$(json_escape "$TOPIC")
ESCAPED_CONTENT=$(json_escape "$CONTENT")
ESCAPED_PROJECT=$(json_escape "$PROJECT")

# Build artifacts array — escape each element
if [[ -n "$ARTIFACTS" ]]; then
  ARTIFACTS_JSON="["
  FIRST=true
  IFS=',' read -ra ART_ARRAY <<< "$ARTIFACTS"
  for art in "${ART_ARRAY[@]}"; do
    escaped_art=$(json_escape "$art")
    if $FIRST; then
      ARTIFACTS_JSON="${ARTIFACTS_JSON}\"${escaped_art}\""
      FIRST=false
    else
      ARTIFACTS_JSON="${ARTIFACTS_JSON},\"${escaped_art}\""
    fi
  done
  ARTIFACTS_JSON="${ARTIFACTS_JSON}]"
else
  ARTIFACTS_JSON="[]"
fi

# Build JSON line with all fields escaped
JSON_LINE="{\"ts\":\"$TS\",\"session\":\"$ESCAPED_SESSION\",\"engine\":\"$ENGINE\",\"topic\":\"$ESCAPED_TOPIC\",\"type\":\"$TYPE\",\"content\":\"$ESCAPED_CONTENT\",\"artifacts\":$ARTIFACTS_JSON,\"project\":\"$ESCAPED_PROJECT\"}"

# Ensure directory exists
mkdir -p "$(dirname "$DISCOVERIES")"

# Append
echo "$JSON_LINE" >> "$DISCOVERIES"

# Output what was written
echo "$JSON_LINE"
echo "OK: Discovery appended to $DISCOVERIES" >&2
