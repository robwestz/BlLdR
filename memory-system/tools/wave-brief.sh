#!/usr/bin/env bash
# wave-brief.sh — Generate hot-tier wave brief (<800 tokens)
#
# Produces a compact context snapshot for wave start:
#   - Current project phase + status (1 line)
#   - Last 3 discoveries (what was just learned)
#   - Active warnings/guardrails (if any)
#   - Next action pointer
#
# This is the MINIMUM context needed to resume work. Designed to be
# always-loaded without contributing to autocompaction.
#
# Usage:
#   wave-brief.sh                    # Output to stdout
#   wave-brief.sh > memory-system/context/wave-brief.md
#
# Output: Compact markdown, always <800 tokens.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$MEMORY_ROOT/.." && pwd)"
DISCOVERIES="$MEMORY_ROOT/continuum/discoveries.jsonl"
GUARDRAILS="$MEMORY_ROOT/../vault/constraints/security.md"

# --- Resolve Python ---
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
  PYTHON_CMD="python"
else
  echo "ERROR: Python required" >&2
  exit 1
fi

# Windows path conversion
winpath() {
  if command -v cygpath &>/dev/null; then
    cygpath -w "$1"
  else
    echo "$1"
  fi
}

# --- Resolve PROJECT.md (search in priority order, not hardcoded) ---
PROJECT_MD=""
CANDIDATES=(
  "$MEMORY_ROOT/../PROJECT.md"
  "$WORKSPACE_ROOT/PROJECT.md"
)

for _candidate in "${CANDIDATES[@]}"; do
  if [[ -f "$_candidate" ]]; then
    PROJECT_MD="$_candidate"
    break
  fi
done

if [[ -z "$PROJECT_MD" ]]; then
  PROJECT_MD="/dev/null"  # No PROJECT.md found — brief will show "Unknown" phase
fi

DISCOVERIES_W=$(winpath "$DISCOVERIES")
PROJECT_W=$(winpath "$PROJECT_MD")
GUARDRAILS_W=$(winpath "$GUARDRAILS")

HANDOFF="$MEMORY_ROOT/context/handoff.md"
HANDOFF_W=$(winpath "$HANDOFF")

export _BUILDR_DISC="$DISCOVERIES_W"
export _BUILDR_PROJ="$PROJECT_W"
export _BUILDR_GUARD="$GUARDRAILS_W"
export _BUILDR_HANDOFF="$HANDOFF_W"

"$PYTHON_CMD" << 'PYEOF'
import json, os, sys
from datetime import datetime, timezone

disc_path = os.environ['_BUILDR_DISC']
proj_path = os.environ['_BUILDR_PROJ']
guard_path = os.environ['_BUILDR_GUARD']
handoff_path = os.environ.get('_BUILDR_HANDOFF', '')

# --- Extract project phase from PROJECT.md ---
phase_line = "Unknown"
next_items = []
try:
    with open(proj_path, encoding='utf-8') as f:
        in_open = False
        for line in f:
            line = line.rstrip()
            if line.startswith("**Fas:**") or line.startswith("**Phase:**"):
                phase_line = line.replace("**Fas:**", "").replace("**Phase:**", "").strip()
            elif "Öppet" in line or "Framtida" in line or "Next" in line:
                in_open = True
            elif in_open and line.startswith("- "):
                next_items.append(line[2:].strip())
                if len(next_items) >= 3:
                    in_open = False
except FileNotFoundError:
    pass

# --- Last 3 discoveries ---
discoveries = []
try:
    with open(disc_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    discoveries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
except FileNotFoundError:
    pass

recent = discoveries[-3:]

# --- Guardrail warnings ---
warnings = []
try:
    with open(guard_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("- ") and any(kw in line.lower() for kw in ['error', 'crash', 'oom', 'timeout', 'injection']):
                warnings.append(line[2:].strip())
except FileNotFoundError:
    pass

# --- Staleness check: handoff age ---
stale_warning = None
try:
    if handoff_path and os.path.isfile(handoff_path):
        handoff_mtime = os.path.getmtime(handoff_path)
        handoff_age_h = (datetime.now(timezone.utc).timestamp() - handoff_mtime) / 3600
        if handoff_age_h > 24:
            stale_warning = f"STALE MEMORY: Last handoff was {int(handoff_age_h)}h ago. Run wave-end.sh."
    elif not handoff_path or not os.path.exists(handoff_path):
        if discoveries:
            last_ts = discoveries[-1].get('ts', '')
            if last_ts:
                try:
                    last_dt = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
                    age_h = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
                    if age_h > 48:
                        stale_warning = f"STALE MEMORY: Last discovery was {int(age_h)}h ago. No handoff found."
                except:
                    pass
except:
    pass

# --- Output compact brief ---
if stale_warning:
    print(f"**{stale_warning}**")
    print()

print("### Wave Status")
print(f"Phase: {phase_line}")
print(f"Discoveries: {len(discoveries)} total")
print(f"Latest: {discoveries[-1].get('ts', '?')[:10] if discoveries else 'N/A'}")
print()

print("### Latest 3 Discoveries")
for d in recent:
    topic = d.get('topic', '?')
    content = d.get('content', '')
    if len(content) > 120:
        content = content[:117] + "..."
    print(f"- [{topic}] {content}")
print()

if warnings:
    print("### Active Warnings")
    for w in warnings[:3]:
        if len(w) > 100:
            w = w[:97] + "..."
        print(f"- {w}")
    print()

if next_items:
    print("### Next Steps")
    for item in next_items[:3]:
        if len(item) > 100:
            item = item[:97] + "..."
        print(f"- {item}")
    print()

print(f"_Brief generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC_")
PYEOF

unset _BUILDR_DISC _BUILDR_PROJ _BUILDR_GUARD _BUILDR_HANDOFF
