#!/usr/bin/env bash
# _common.sh — Shared helper functions for memory-system/tools/
#
# Usage: source "$SCRIPT_DIR/_common.sh"

# Windows path conversion (cygpath if available, passthrough otherwise)
winpath() {
  if command -v cygpath &>/dev/null; then
    cygpath -w "$1"
  else
    echo "$1"
  fi
}

# Resolve Python command (python3 preferred, fallback python)
resolve_python() {
  if command -v python3 &>/dev/null; then
    echo "python3"
  elif command -v python &>/dev/null; then
    echo "python"
  else
    echo "ERROR: Python required" >&2
    return 1
  fi
}

# Read a value from config/defaults.yaml (simple key.subkey lookup)
# Usage: read_arg "session.auto_handoff" [default_value]
# Returns: the value, or default_value if not found, or empty string
read_arg() {
  local keypath="${1:-}"
  local default_val="${2:-}"
  local _SCRIPT_DIR
  _SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local _MEMORY_ROOT
  _MEMORY_ROOT="$(cd "$_SCRIPT_DIR/.." && pwd)"
  local args_file="$_MEMORY_ROOT/config/defaults.yaml"

  if [[ ! -f "$args_file" ]]; then
    echo "$default_val"
    return 0
  fi

  local _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -z "$_PY" ]]; then
    echo "$default_val"
    return 0
  fi

  local result
  result=$(export _ARGS_FILE="$args_file" _ARGS_KEY="$keypath" _ARGS_DEFAULT="$default_val"; "$_PY" -c "
import os, sys

def parse_yaml_simple(path):
    \"\"\"Minimal YAML parser for flat/nested key:value files (no arrays, no anchors).\"\"\"
    data = {}
    stack = [data]
    indent_stack = [-1]
    with open(path, encoding='utf-8') as f:
        for line in f:
            stripped = line.rstrip()
            if not stripped or stripped.lstrip().startswith('#'):
                continue
            indent = len(line) - len(line.lstrip())
            content = stripped.lstrip()
            while indent <= indent_stack[-1] and len(indent_stack) > 1:
                indent_stack.pop()
                stack.pop()
            if ':' in content:
                key, _, val = content.partition(':')
                key = key.strip()
                val = val.strip()
                if val:
                    stack[-1][key] = val
                else:
                    new_dict = {}
                    stack[-1][key] = new_dict
                    stack.append(new_dict)
                    indent_stack.append(indent)
    return data

try:
    data = parse_yaml_simple(os.environ['_ARGS_FILE'])
    keys = os.environ['_ARGS_KEY'].split('.')
    current = data
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            print(os.environ.get('_ARGS_DEFAULT', ''))
            sys.exit(0)
    print(current)
except Exception:
    print(os.environ.get('_ARGS_DEFAULT', ''))
" 2>/dev/null) || result="$default_val"
  echo "$result"
}
