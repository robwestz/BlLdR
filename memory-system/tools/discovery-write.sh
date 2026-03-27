#!/usr/bin/env bash
# discovery-write.sh — Append a discovery to memory-system/continuum/discoveries.jsonl
#
# Usage:
#   discovery-write.sh --session SESSION --engine ENGINE --topic TOPIC --content "CONTENT" [--type TYPE] [--direction DIRECTION] [--artifacts "file1,file2"] [--project PROJECT]
#
# Types: fact, preference, insight (default), event, decision, error
#
# Example:
#   discovery-write.sh --session opus-2 --engine claude --topic model-router --type decision --content "Domain match should precede complexity match" --artifacts "memory-system/config/routing.json"
#
# Output: The appended JSON line (to stdout), and writes to discoveries.jsonl

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DISCOVERIES="$MEMORY_ROOT/continuum/discoveries.jsonl"

# Defaults
SESSION=""
ENGINE=""
TOPIC=""
CONTENT=""
TYPE="insight"
DIRECTION="executing"
ARTIFACTS=""
PROJECT="buildr"

# Valid discovery types
VALID_TYPES="fact preference insight event decision error"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)   SESSION="$2"; shift 2 ;;
    --engine)    ENGINE="$2"; shift 2 ;;
    --topic)     TOPIC="$2"; shift 2 ;;
    --content)   CONTENT="$2"; shift 2 ;;
    --type)      TYPE="$2"; shift 2 ;;
    --direction) DIRECTION="$2"; shift 2 ;;
    --artifacts) ARTIFACTS="$2"; shift 2 ;;
    --project)   PROJECT="$2"; shift 2 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      echo "Usage: discovery-write.sh --session SESSION --engine ENGINE --topic TOPIC --content \"CONTENT\" [--type TYPE] [--direction DIRECTION] [--artifacts \"f1,f2\"] [--project PROJECT]" >&2
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

VALID_DIRECTIONS="planning executing reviewing debugging"
DIR_VALID=false
for _d in $VALID_DIRECTIONS; do
  [[ "$DIRECTION" == "$_d" ]] && DIR_VALID=true
done
if [[ "$DIR_VALID" != true ]]; then
  echo "ERROR: --direction must be one of: $VALID_DIRECTIONS (got: $DIRECTION)" >&2
  exit 1
fi

# --- Engine validation (config-driven) ---
# Read whitelist from defaults.json, fallback to hardcoded if config unavailable
ENGINE_VALID=false
if [[ -f "$MEMORY_ROOT/config/defaults.json" ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -n "$_PY" ]]; then
    export _BUILDR_DEFAULTS="$MEMORY_ROOT/config/defaults.json"
    WHITELIST=$("$_PY" -c "
import json, os
try:
    with open(os.environ['_BUILDR_DEFAULTS'], encoding='utf-8') as f:
        cfg = json.load(f)
    wl = cfg.get('security', {}).get('engine_whitelist', ['claude','gemini','codex','sonnet'])
    print(' '.join(wl))
except Exception:
    print('claude gemini codex sonnet')
" 2>/dev/null) || WHITELIST="claude gemini codex sonnet"
    unset _BUILDR_DEFAULTS
  else
    WHITELIST="claude gemini codex sonnet"
  fi
else
  WHITELIST="claude gemini codex sonnet"
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
if [[ -f "$MEMORY_ROOT/config/defaults.json" ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -n "$_PY" ]]; then
    export _BUILDR_DEFAULTS="$MEMORY_ROOT/config/defaults.json"
    _DENY_CFG=$("$_PY" -c "
import json, os
try:
    with open(os.environ['_BUILDR_DEFAULTS'], encoding='utf-8') as f:
        cfg = json.load(f)
    print('true' if cfg.get('security', {}).get('deny_write_if_secret_like', True) else 'false')
except Exception:
    print('true')
" 2>/dev/null) || _DENY_CFG="true"
    unset _BUILDR_DEFAULTS
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
ESCAPED_DIRECTION=$(json_escape "$DIRECTION")

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
JSON_LINE="{\"ts\":\"$TS\",\"session\":\"$ESCAPED_SESSION\",\"engine\":\"$ENGINE\",\"topic\":\"$ESCAPED_TOPIC\",\"type\":\"$TYPE\",\"direction\":\"$ESCAPED_DIRECTION\",\"content\":\"$ESCAPED_CONTENT\",\"artifacts\":$ARTIFACTS_JSON,\"project\":\"$ESCAPED_PROJECT\"}"

# Ensure directory exists
mkdir -p "$(dirname "$DISCOVERIES")"

# Append
echo "$JSON_LINE" >> "$DISCOVERIES"

# Output what was written
echo "$JSON_LINE"
echo "OK: Discovery appended to $DISCOVERIES" >&2
