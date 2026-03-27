#!/usr/bin/env bash
# session-end.sh — One-command session end
#
# Does everything needed at the end of a session:
#   1. Runs auto-discovery (safety net — catch any missed commits)
#   2. Creates handoff contract
#   3. Generates session brief (for next session's hot tier)
#   4. Distills discoveries (compresses warm tier)
#   5. Injects discoveries into CLAUDE.md
#   6. Creates checkpoint (if enough new discoveries)
#   7. Ends session tracking
#
# Usage:
#   session-end.sh --session opus-9 --summary "Built auth flow"
#   session-end.sh --session opus-9 --summary "..." --next "Add tests;Deploy"
#   session-end.sh --session opus-9 --summary "..." --files "src/auth.ts,src/middleware.ts"
#   session-end.sh --session opus-9 --summary "..." --skip-inject
#
# Required: --session and --summary (passed through to session-handoff.sh)
# Optional: --next, --files, --skip-inject, --skip-distill, --skip-checkpoint

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONTEXT_DIR="$ULTIMA_ROOT/context"

SKIP_INJECT=false
SKIP_DISTILL=false
SKIP_CHECKPOINT=false
HANDOFF_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-inject)     SKIP_INJECT=true; shift ;;
    --skip-distill)    SKIP_DISTILL=true; shift ;;
    --skip-checkpoint) SKIP_CHECKPOINT=true; shift ;;
    *)                 HANDOFF_ARGS+=("$1"); shift ;;
  esac
done

# --- Step 1: Auto-discovery (safety net) ---
if [[ -f "$SCRIPT_DIR/auto-discovery.sh" ]]; then
  echo "=== Mining git commits ===" >&2
  bash "$SCRIPT_DIR/auto-discovery.sh" > /dev/null 2>&1 || {
    echo "WARNING: auto-discovery.sh failed (non-blocking)" >&2
  }
fi

# --- Step 2: Create handoff contract ---
echo "=== Creating handoff ===" >&2
bash "$SCRIPT_DIR/session-handoff.sh" "${HANDOFF_ARGS[@]}"

# --- Step 3: Generate session brief ---
echo "=== Generating session brief ===" >&2
if [[ -x "$SCRIPT_DIR/session-brief.sh" ]]; then
  bash "$SCRIPT_DIR/session-brief.sh" > "$CONTEXT_DIR/session-brief.md" 2>/dev/null || {
    echo "WARNING: session-brief.sh failed (non-blocking)" >&2
  }
else
  echo "WARNING: session-brief.sh not found" >&2
fi

# --- Step 4: Distill discoveries ---
if [[ "$SKIP_DISTILL" != true ]]; then
  echo "=== Distilling discoveries ===" >&2
  if [[ -x "$SCRIPT_DIR/distill-discoveries.sh" ]]; then
    bash "$SCRIPT_DIR/distill-discoveries.sh" > "$CONTEXT_DIR/distilled.md" 2>/dev/null || {
      echo "WARNING: distill-discoveries.sh failed (non-blocking)" >&2
    }
  fi
fi

# --- Step 5: Inject to CLAUDE.md ---
if [[ "$SKIP_INJECT" != true ]]; then
  CLAUDE_MD="$ULTIMA_ROOT/../CLAUDE.md"
  if [[ -f "$CLAUDE_MD" ]]; then
    echo "=== Injecting discoveries to CLAUDE.md ===" >&2
    bash "$SCRIPT_DIR/inject-context.sh" 2>/dev/null || {
      echo "WARNING: inject-context.sh failed (non-blocking)" >&2
    }
  fi
fi

# --- Step 6: Checkpoint (auto mode) ---
if [[ "$SKIP_CHECKPOINT" != true && -f "$SCRIPT_DIR/checkpoint.sh" ]]; then
  echo "=== Checking checkpoint threshold ===" >&2
  bash "$SCRIPT_DIR/checkpoint.sh" --auto 2>&1 | grep -v '^/' >&2 || true
fi

# --- Step 7: End session tracking ---
if [[ -f "$SCRIPT_DIR/session-track.sh" ]]; then
  echo "=== Ending session tracking ===" >&2
  bash "$SCRIPT_DIR/session-track.sh" --end 2>&1 >&2 || {
    echo "WARNING: session-track.sh --end failed (non-blocking)" >&2
  }
fi

echo "=== Session end complete ===" >&2
