#!/usr/bin/env bash
# doctor.sh — Health check for memory-system/ setup
#
# Verifies that the memory system is correctly installed and functional.
# Run after installation, after changes, or periodically as a sanity check.
#
# Usage:
#   doctor.sh              # Check current memory-system/ setup
#   doctor.sh --verbose    # Show passing checks too
#
# Exit codes:
#   0 = all checks passed (OK)
#   1 = one or more issues found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"

VERBOSE=false
[[ "${1:-}" == "--verbose" ]] && VERBOSE=true

ISSUES=()
PASS=0

# Colors (if terminal)
if [[ -t 1 ]]; then
  GREEN='\033[0;32m'
  RED='\033[0;31m'
  YELLOW='\033[0;33m'
  BOLD='\033[1m'
  RESET='\033[0m'
else
  GREEN="" RED="" YELLOW="" BOLD="" RESET=""
fi

_pass() {
  PASS=$((PASS + 1))
  if [[ "$VERBOSE" == true ]]; then
    echo -e "  ${GREEN}OK${RESET}  $1"
  fi
}

_fail() {
  ISSUES+=("$1: $2")
  echo -e "  ${RED}FAIL${RESET}  $1"
  echo -e "        ${YELLOW}Fix: $2${RESET}"
}

echo -e "${BOLD}Buildr Memory System — Health Check${RESET}"
echo "Root: $MEMORY_ROOT"
echo ""

# --- 1. Directory structure ---
echo -e "${BOLD}[directories]${RESET}"
for dir in config context continuum tools templates; do
  if [[ -d "$MEMORY_ROOT/$dir" ]]; then
    _pass "$dir/"
  else
    _fail "$dir/" "mkdir -p $MEMORY_ROOT/$dir"
  fi
done

# --- 2. Config: defaults.json parseable ---
echo -e "${BOLD}[config]${RESET}"
DEFAULTS="$MEMORY_ROOT/config/defaults.json"
if [[ -f "$DEFAULTS" ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -n "$_PY" ]]; then
    if _BUILDR_DEFAULTS="$DEFAULTS" "$_PY" -c "import json, os; json.load(open(os.environ['_BUILDR_DEFAULTS'], encoding='utf-8'))" 2>/dev/null; then
      _pass "defaults.json parses as valid JSON"
    else
      _fail "defaults.json" "Fix JSON syntax errors in $DEFAULTS"
    fi
  else
    _fail "python" "Install python3 (required for JSON validation)"
  fi
else
  _fail "defaults.json" "Create $DEFAULTS"
fi

# --- 3. Discoveries: each line valid JSON ---
echo -e "${BOLD}[continuum]${RESET}"
DISC="$MEMORY_ROOT/continuum/discoveries.jsonl"
if [[ -f "$DISC" ]]; then
  if [[ ! -s "$DISC" ]]; then
    _pass "discoveries.jsonl exists (empty — ready for first discovery)"
  else
    _PY=""
    command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
    if [[ -n "$_PY" ]]; then
      BAD_LINES=$(_BUILDR_DISC="$DISC" "$_PY" -c "
import json, os
bad = []
with open(os.environ['_BUILDR_DISC'], encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            bad.append(f'line {i}: {e}')
if bad:
    print('\n'.join(bad[:5]))
    raise SystemExit(1)
" 2>&1) || true
      if [[ -z "$BAD_LINES" ]]; then
        LINE_COUNT=$(grep -c . "$DISC" 2>/dev/null || echo 0)
        _pass "discoveries.jsonl ($LINE_COUNT entries, all valid JSON)"
      else
        _fail "discoveries.jsonl" "Invalid JSON lines:\n$BAD_LINES"
      fi
    else
      _pass "discoveries.jsonl exists (skipped JSON validation — no python)"
    fi
  fi
else
  _fail "discoveries.jsonl" "touch $DISC"
fi

# --- 4. MEMORY.md marker block ---
echo -e "${BOLD}[injection markers]${RESET}"
MEMORY_MD="$WORKSPACE_ROOT/MEMORY.md"
if [[ -f "$MEMORY_MD" ]]; then
  if grep -q '<!-- BUILDR-INJECT-START -->' "$MEMORY_MD" 2>/dev/null && \
     grep -q '<!-- BUILDR-INJECT-END -->' "$MEMORY_MD" 2>/dev/null; then
    _pass "MEMORY.md has BUILDR-INJECT markers"
  else
    _fail "MEMORY.md markers" "Add <!-- BUILDR-INJECT-START --> and <!-- BUILDR-INJECT-END --> to $MEMORY_MD"
  fi
else
  [[ "$VERBOSE" == true ]] && echo -e "  ${YELLOW}SKIP${RESET}  MEMORY.md not found (optional — only needed for memory-inject.sh)"
fi

# --- 5. Vault ---
echo -e "${BOLD}[vault]${RESET}"
if [[ -f "$MEMORY_ROOT/../vault/INDEX.md" ]]; then
  _pass "vault/INDEX.md"
else
  _fail "vault/INDEX.md" "Create $MEMORY_ROOT/../vault/INDEX.md"
fi

# --- 6. Engines ---
echo -e "${BOLD}[engines]${RESET}"
if [[ -f "$MEMORY_ROOT/../engines/imperfektum_engine.py" ]]; then
  _pass "engines/imperfektum_engine.py"
else
  _fail "engines/imperfektum_engine.py" "Create $MEMORY_ROOT/../engines/imperfektum_engine.py"
fi

# --- 7. Tools executable ---
echo -e "${BOLD}[tools]${RESET}"
for tool in discovery-write.sh context-load.sh memory-inject.sh wave-brief.sh discovery-distill.sh wave-handoff.sh discovery-mine.sh wave-track.sh checkpoint.sh wave-start.sh wave-end.sh; do
  TOOL_PATH="$MEMORY_ROOT/tools/$tool"
  if [[ -f "$TOOL_PATH" ]]; then
    if [[ -x "$TOOL_PATH" ]]; then
      _pass "tools/$tool (executable)"
    else
      _fail "tools/$tool" "chmod +x $TOOL_PATH"
    fi
  else
    _fail "tools/$tool" "Missing tool — reinstall from kit"
  fi
done

# --- 8. Staleness check ---
echo -e "${BOLD}[staleness]${RESET}"
HANDOFF_FILE="$MEMORY_ROOT/context/handoff.md"
if [[ -f "$HANDOFF_FILE" ]]; then
  _MTIME=0
  if stat --version &>/dev/null 2>&1; then
    _MTIME=$(stat -c %Y "$HANDOFF_FILE" 2>/dev/null || echo 0)
  else
    _MTIME=$(stat -f %m "$HANDOFF_FILE" 2>/dev/null || echo 0)
  fi
  _NOW=$(date +%s)
  _AGE_H=$(( (_NOW - _MTIME) / 3600 ))
  if [[ "$_AGE_H" -gt 48 ]]; then
    _fail "handoff staleness" "Handoff is ${_AGE_H}h old. Run wave-end.sh"
  elif [[ "$_AGE_H" -gt 24 ]]; then
    if [[ "$VERBOSE" == true ]]; then
      echo -e "  ${YELLOW}WARN${RESET}  Handoff is ${_AGE_H}h old (>24h). Consider running wave-end.sh"
    fi
    _pass "handoff age (${_AGE_H}h — approaching stale)"
  else
    _pass "handoff age (${_AGE_H}h — fresh)"
  fi
else
  if [[ -f "$DISC" && -s "$DISC" ]]; then
    _fail "handoff missing" "No handoff.md found. Run wave-end.sh to create one"
  else
    _pass "handoff not required (no discoveries yet)"
  fi
fi

# --- 9. Sessions directory ---
echo -e "${BOLD}[sessions]${RESET}"
SESSIONS_DIR="$MEMORY_ROOT/continuum/sessions"
if [[ -d "$SESSIONS_DIR" ]]; then
  shopt -s nullglob
  SESSION_FILES=("$SESSIONS_DIR"/*.json)
  shopt -u nullglob
  SESSION_COUNT=${#SESSION_FILES[@]}
  _pass "continuum/sessions/ ($SESSION_COUNT session files)"
else
  if [[ "$VERBOSE" == true ]]; then
    echo -e "  ${YELLOW}WARN${RESET}  continuum/sessions/ missing — mkdir -p $SESSIONS_DIR"
  fi
  _pass "sessions/ not yet created (will be created by wave-track.sh)"
fi

# --- 10. Checkpoints directory ---
echo -e "${BOLD}[checkpoints]${RESET}"
CP_DIR="$MEMORY_ROOT/continuum/checkpoints"
if [[ -d "$CP_DIR" ]]; then
  shopt -s nullglob
  CHECKPOINT_FILES=("$CP_DIR"/*/manifest.json)
  shopt -u nullglob
  CP_COUNT=${#CHECKPOINT_FILES[@]}
  _pass "continuum/checkpoints/ ($CP_COUNT checkpoints)"
else
  _pass "checkpoints/ not yet created (will be created by checkpoint.sh)"
fi

# --- 11. Dependencies ---
echo -e "${BOLD}[dependencies]${RESET}"
if command -v python3 &>/dev/null || command -v python &>/dev/null; then
  PY_VER=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
  _pass "Python available ($PY_VER)"
else
  _fail "python" "Install Python 3.x (required for distill, context-load JSON, inject)"
fi

if command -v bash &>/dev/null; then
  _pass "bash available"
fi

# --- Summary ---
echo ""
TOTAL=$((PASS + ${#ISSUES[@]}))
if [[ ${#ISSUES[@]} -eq 0 ]]; then
  echo -e "${GREEN}${BOLD}OK${RESET} — All $TOTAL checks passed."
  exit 0
else
  echo -e "${RED}${BOLD}${#ISSUES[@]} issue(s)${RESET} found ($PASS passed, ${#ISSUES[@]} failed):"
  echo ""
  for issue in "${ISSUES[@]}"; do
    echo "  - $issue"
  done
  exit 1
fi
