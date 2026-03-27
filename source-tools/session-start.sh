#!/usr/bin/env bash
# session-start.sh — One-command session start
#
# Does everything needed at the beginning of a session:
#   1. Runs auto-discovery (mines git commits, 0 tokens)
#   2. Starts session tracking
#   3. Runs doctor.sh (quick health check, non-blocking)
#   4. Auto-selects tier and loads context
#   5. Prints the assembled context to stdout
#
# Usage:
#   session-start.sh                      # Auto-tier, default behavior
#   session-start.sh --tier hot           # Force specific tier
#   session-start.sh --budget 1500        # Budget mode
#   session-start.sh --skip-doctor        # Skip health check
#   session-start.sh --engine gemini      # Set engine for session tracking
#
# Output: Context printed to stdout. Doctor/tracking info to stderr.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKIP_DOCTOR=false
ENGINE="claude"
CONTEXT_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-doctor) SKIP_DOCTOR=true; shift ;;
    --engine)      ENGINE="$2"; shift 2 ;;
    *)             CONTEXT_ARGS+=("$1"); shift ;;
  esac
done

# --- Step 1: Auto-discovery (mine git commits, 0 tokens) ---
if [[ -f "$SCRIPT_DIR/auto-discovery.sh" ]]; then
  bash "$SCRIPT_DIR/auto-discovery.sh" > /dev/null 2>&1 || {
    echo "WARNING: auto-discovery.sh failed (non-blocking)" >&2
  }
fi

# --- Step 2: Start session tracking ---
SESSION_ID=""
if [[ -f "$SCRIPT_DIR/session-track.sh" ]]; then
  SESSION_ID=$(bash "$SCRIPT_DIR/session-track.sh" --start --engine "$ENGINE" 2>/dev/null) || {
    echo "WARNING: session-track.sh --start failed (non-blocking)" >&2
  }
  if [[ -n "$SESSION_ID" ]]; then
    echo "Session: $SESSION_ID" >&2
  fi
fi

# --- Step 3: Quick health check (non-blocking) ---
if [[ "$SKIP_DOCTOR" != true && -f "$SCRIPT_DIR/doctor.sh" ]]; then
  DOCTOR_EXIT=0
  DOCTOR_OUT=$(bash "$SCRIPT_DIR/doctor.sh" 2>&1) || DOCTOR_EXIT=$?

  if [[ "$DOCTOR_EXIT" -ne 0 ]]; then
    echo "=== Doctor found issues (non-blocking) ===" >&2
    echo "$DOCTOR_OUT" | grep -E "FAIL|Fix:" >&2
    echo "=== Run 'doctor.sh --verbose' for details ===" >&2
    echo "" >&2
  fi
fi

# --- Step 4: Load context (auto-tier or explicit) ---
exec bash "$SCRIPT_DIR/context-load.sh" "${CONTEXT_ARGS[@]}"
