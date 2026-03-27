#!/usr/bin/env bash
# wave-end.sh — One-command wave end
#
# Does everything needed at the end of a wave:
#   1. Runs discovery-mine.sh (safety net — catch any missed commits)
#   2. Creates handoff contract
#   3. Generates wave brief (for next wave's hot tier)
#   4. Distills discoveries (compresses warm tier)
#   5. Injects discoveries into MEMORY.md
#   6. Creates checkpoint (if enough new discoveries)
#   7. Ends wave tracking
#
# Usage:
#   wave-end.sh --session opus-9 --summary "Built auth flow"
#   wave-end.sh --session opus-9 --summary "..." --next "Add tests;Deploy"
#   wave-end.sh --session opus-9 --summary "..." --files "src/auth.ts,src/middleware.ts"
#   wave-end.sh --session opus-9 --summary "..." --skip-inject
#
# Required: --session and --summary (passed through to wave-handoff.sh)
# Optional: --next, --files, --skip-inject, --skip-distill, --skip-checkpoint

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONTEXT_DIR="$MEMORY_ROOT/context"

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

# --- Step 1: Mine git commits ---
if [[ -f "$SCRIPT_DIR/discovery-mine.sh" ]]; then
  echo "=== Mining git commits ===" >&2
  bash "$SCRIPT_DIR/discovery-mine.sh" > /dev/null 2>&1 || {
    echo "WARNING: discovery-mine.sh failed (non-blocking)" >&2
  }
fi

# --- Step 2: Create wave handoff ---
echo "=== Creating handoff ===" >&2
bash "$SCRIPT_DIR/wave-handoff.sh" "${HANDOFF_ARGS[@]}"

# --- Step 3: Generate wave brief ---
echo "=== Generating wave brief ===" >&2
if [[ -x "$SCRIPT_DIR/wave-brief.sh" ]]; then
  bash "$SCRIPT_DIR/wave-brief.sh" > "$CONTEXT_DIR/wave-brief.md" 2>/dev/null || {
    echo "WARNING: wave-brief.sh failed (non-blocking)" >&2
  }
else
  echo "WARNING: wave-brief.sh not found" >&2
fi

# --- Step 4: Distill discoveries ---
if [[ "$SKIP_DISTILL" != true ]]; then
  echo "=== Distilling discoveries ===" >&2
  if [[ -x "$SCRIPT_DIR/discovery-distill.sh" ]]; then
    bash "$SCRIPT_DIR/discovery-distill.sh" > "$CONTEXT_DIR/distilled.md" 2>/dev/null || {
      echo "WARNING: discovery-distill.sh failed (non-blocking)" >&2
    }
  fi
fi

# --- Step 5: Inject to MEMORY.md ---
if [[ "$SKIP_INJECT" != true ]]; then
  MEMORY_MD="$MEMORY_ROOT/../MEMORY.md"
  if [[ -f "$MEMORY_MD" ]]; then
    echo "=== Injecting discoveries to MEMORY.md ===" >&2
    bash "$SCRIPT_DIR/memory-inject.sh" 2>/dev/null || {
      echo "WARNING: memory-inject.sh failed (non-blocking)" >&2
    }
  fi
fi

# --- Step 6: Checkpoint (auto mode) ---
if [[ "$SKIP_CHECKPOINT" != true && -f "$SCRIPT_DIR/checkpoint.sh" ]]; then
  echo "=== Checking checkpoint threshold ===" >&2
  bash "$SCRIPT_DIR/checkpoint.sh" --auto 2>&1 | grep -v '^/' >&2 || true
fi

# --- Step 7: End wave tracking ---
if [[ -f "$SCRIPT_DIR/wave-track.sh" ]]; then
  echo "=== Ending wave tracking ===" >&2
  bash "$SCRIPT_DIR/wave-track.sh" --end 2>&1 >&2 || {
    echo "WARNING: wave-track.sh --end failed (non-blocking)" >&2
  }
fi

echo "=== Wave end complete ===" >&2
