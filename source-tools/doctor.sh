#!/usr/bin/env bash
# doctor.sh — Health check for .ultima/ setup
#
# Verifies that the memory kit is correctly installed and functional.
# Run after installation, after changes, or periodically as a sanity check.
#
# Usage:
#   doctor.sh              # Check current .ultima/ setup
#   doctor.sh --verbose    # Show passing checks too
#
# Exit codes:
#   0 = all checks passed (OK)
#   1 = one or more issues found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$ULTIMA_ROOT/.." && pwd)"

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

echo -e "${BOLD}Ultima Memory Kit — Health Check${RESET}"
echo "Root: $ULTIMA_ROOT"
echo ""

# --- 1. Directory structure ---
echo -e "${BOLD}[directories]${RESET}"
for dir in config context continuum identity tools; do
  if [[ -d "$ULTIMA_ROOT/$dir" ]]; then
    _pass "$dir/"
  else
    _fail "$dir/" "mkdir -p $ULTIMA_ROOT/$dir"
  fi
done

# --- 2. Config: defaults.json parseable ---
echo -e "${BOLD}[config]${RESET}"
DEFAULTS="$ULTIMA_ROOT/config/defaults.json"
if [[ -f "$DEFAULTS" ]]; then
  _PY=""
  command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
  if [[ -n "$_PY" ]]; then
    if _ULTIMA_DEFAULTS="$DEFAULTS" "$_PY" -c "import json, os; json.load(open(os.environ['_ULTIMA_DEFAULTS'], encoding='utf-8'))" 2>/dev/null; then
      _pass "defaults.json parses as valid JSON"
    else
      _fail "defaults.json" "Fix JSON syntax errors in $DEFAULTS"
    fi
  else
    _fail "python" "Install python3 (required for JSON validation)"
  fi
else
  _fail "defaults.json" "cp config/defaults.json template to $DEFAULTS"
fi

# --- 3. Discoveries: each line valid JSON ---
echo -e "${BOLD}[continuum]${RESET}"
DISC="$ULTIMA_ROOT/continuum/discoveries.jsonl"
if [[ -f "$DISC" ]]; then
  if [[ ! -s "$DISC" ]]; then
    _pass "discoveries.jsonl exists (empty — ready for first discovery)"
  else
    _PY=""
    command -v python3 &>/dev/null && _PY="python3" || { command -v python &>/dev/null && _PY="python"; }
    if [[ -n "$_PY" ]]; then
      BAD_LINES=$(_ULTIMA_DISC="$DISC" "$_PY" -c "
import json, os
bad = []
with open(os.environ['_ULTIMA_DISC'], encoding='utf-8') as f:
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

# --- 4. CLAUDE.md marker block ---
echo -e "${BOLD}[injection markers]${RESET}"
CLAUDE_MD="$WORKSPACE_ROOT/CLAUDE.md"
if [[ -f "$CLAUDE_MD" ]]; then
  if grep -q '<!-- MEMORY-INJECT-START -->' "$CLAUDE_MD" 2>/dev/null && \
     grep -q '<!-- MEMORY-INJECT-END -->' "$CLAUDE_MD" 2>/dev/null; then
    _pass "CLAUDE.md has MEMORY-INJECT markers"
  else
    _fail "CLAUDE.md markers" "Add <!-- MEMORY-INJECT-START --> and <!-- MEMORY-INJECT-END --> to $CLAUDE_MD"
  fi
else
  [[ "$VERBOSE" == true ]] && echo -e "  ${YELLOW}SKIP${RESET}  CLAUDE.md not found (optional — only needed for inject-context.sh)"
fi

# --- 5. Identity files ---
echo -e "${BOLD}[identity]${RESET}"
for id_file in SOUL.md USER.md AGENTS.md; do
  if [[ -f "$ULTIMA_ROOT/identity/$id_file" ]]; then
    if [[ -s "$ULTIMA_ROOT/identity/$id_file" ]]; then
      _pass "identity/$id_file"
    else
      _fail "identity/$id_file" "File is empty — fill in content"
    fi
  else
    _fail "identity/$id_file" "Create $ULTIMA_ROOT/identity/$id_file"
  fi
done

# --- 6. Tools executable ---
echo -e "${BOLD}[tools]${RESET}"
for tool in continuum-write.sh context-load.sh inject-context.sh session-brief.sh distill-discoveries.sh session-handoff.sh auto-discovery.sh session-track.sh checkpoint.sh; do
  TOOL_PATH="$ULTIMA_ROOT/tools/$tool"
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

# --- 7. Staleness check ---
echo -e "${BOLD}[staleness]${RESET}"
HANDOFF_FILE="$ULTIMA_ROOT/context/handoff.md"
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
    _fail "handoff staleness" "Handoff is ${_AGE_H}h old. Run session-end.sh or /memory-maintenance"
  elif [[ "$_AGE_H" -gt 24 ]]; then
    if [[ "$VERBOSE" == true ]]; then
      echo -e "  ${YELLOW}WARN${RESET}  Handoff is ${_AGE_H}h old (>24h). Consider running session-end.sh"
    fi
    _pass "handoff age (${_AGE_H}h — approaching stale)"
  else
    _pass "handoff age (${_AGE_H}h — fresh)"
  fi
else
  if [[ -f "$DISC" && -s "$DISC" ]]; then
    _fail "handoff missing" "No handoff.md found. Run session-end.sh to create one"
  else
    _pass "handoff not required (no discoveries yet)"
  fi
fi

# --- 8. Sessions directory ---
echo -e "${BOLD}[sessions]${RESET}"
SESSIONS_DIR="$ULTIMA_ROOT/continuum/sessions"
if [[ -d "$SESSIONS_DIR" ]]; then
  SESSION_COUNT=$(ls -1 "$SESSIONS_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ' || echo 0)
  _pass "continuum/sessions/ ($SESSION_COUNT session files)"
else
  if [[ "$VERBOSE" == true ]]; then
    echo -e "  ${YELLOW}WARN${RESET}  continuum/sessions/ missing — mkdir -p $SESSIONS_DIR"
  fi
  _pass "sessions/ not yet created (will be created by session-track.sh)"
fi

# --- 9. Checkpoints directory ---
echo -e "${BOLD}[checkpoints]${RESET}"
CP_DIR="$ULTIMA_ROOT/continuum/checkpoints"
if [[ -d "$CP_DIR" ]]; then
  CP_COUNT=$(ls -1d "$CP_DIR"/*/manifest.json 2>/dev/null | wc -l | tr -d ' ' || echo 0)
  _pass "continuum/checkpoints/ ($CP_COUNT checkpoints)"
else
  _pass "checkpoints/ not yet created (will be created by checkpoint.sh)"
fi

# --- 10. Python available ---
# (renumbered from 7)
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
