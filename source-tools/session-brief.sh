#!/usr/bin/env bash
# session-brief.sh — Generate hot-tier session brief (<800 tokens)
#
# Produces a compact context snapshot for session start:
#   - Current project phase + status (1 line)
#   - Last 3 discoveries (what was just learned)
#   - Active warnings/guardrails (if any)
#   - Next action pointer
#
# This is the MINIMUM context needed to resume work. Designed to be
# always-loaded without contributing to autocompaction.
#
# Usage:
#   session-brief.sh                    # Output to stdout
#   session-brief.sh > .ultima/context/session-brief.md
#
# Output: Compact markdown, always <800 tokens.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$ULTIMA_ROOT/.." && pwd)"
DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"
GUARDRAILS="$ULTIMA_ROOT/skills/_guardrails.md"

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
  "$WORKSPACE_ROOT/PROJECT.md"
  "$ULTIMA_ROOT/../PROJECT.md"
  "$WORKSPACE_ROOT/.openclaw/workspace/projects/ultima-claw/PROJECT.md"
)
# Also check upstream.link for parent workspace PROJECT.md
UPSTREAM_LINK="$ULTIMA_ROOT/continuum/upstream.link"
if [[ -f "$UPSTREAM_LINK" ]]; then
  UPSTREAM_W=$(winpath "$UPSTREAM_LINK")
  export _ULTIMA_UP_LINK="$UPSTREAM_W"
  _UP_WS=$("$PYTHON_CMD" << 'PYEOF' 2>/dev/null
import json, os
link_path = os.environ['_ULTIMA_UP_LINK']
with open(link_path, encoding='utf-8') as f:
    print(json.load(f).get('workspace', ''))
PYEOF
  ) || true
  unset _ULTIMA_UP_LINK
  if [[ -n "$_UP_WS" ]]; then
    CANDIDATES+=("$_UP_WS/projects/*/PROJECT.md")
  fi
fi

for _candidate in "${CANDIDATES[@]}"; do
  # Handle glob patterns
  for _resolved in $_candidate; do
    if [[ -f "$_resolved" ]]; then
      PROJECT_MD="$_resolved"
      break 2
    fi
  done
done

if [[ -z "$PROJECT_MD" ]]; then
  PROJECT_MD="/dev/null"  # No PROJECT.md found — brief will show "Unknown" phase
fi

DISCOVERIES_W=$(winpath "$DISCOVERIES")
PROJECT_W=$(winpath "$PROJECT_MD")
GUARDRAILS_W=$(winpath "$GUARDRAILS")

HANDOFF="$ULTIMA_ROOT/context/handoff.md"
HANDOFF_W=$(winpath "$HANDOFF")

export _ULTIMA_DISC="$DISCOVERIES_W"
export _ULTIMA_PROJ="$PROJECT_W"
export _ULTIMA_GUARD="$GUARDRAILS_W"
export _ULTIMA_HANDOFF="$HANDOFF_W"

"$PYTHON_CMD" << 'PYEOF'
import json, os, sys
from datetime import datetime, timezone

disc_path = os.environ['_ULTIMA_DISC']
proj_path = os.environ['_ULTIMA_PROJ']
guard_path = os.environ['_ULTIMA_GUARD']
handoff_path = os.environ.get('_ULTIMA_HANDOFF', '')

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
            stale_warning = f"STALE MEMORY: Last handoff was {int(handoff_age_h)}h ago. Run /memory-maintenance or session-end.sh."
    elif not handoff_path or not os.path.exists(handoff_path):
        if discoveries:
            last_ts = discoveries[-1].get('ts', '')
            if last_ts:
                try:
                    last_dt = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
                    age_h = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
                    if age_h > 48:
                        stale_warning = f"STALE MEMORY: Last discovery was {int(age_h)}h ago. No handoff found."
                except: pass
except: pass

# --- Output compact brief ---
if stale_warning:
    print(f"**{stale_warning}**")
    print()

print("### Status")
print(f"Fas: {phase_line}")
print(f"Discoveries: {len(discoveries)} total")
print(f"Senast: {discoveries[-1].get('ts', '?')[:10] if discoveries else 'N/A'}")
print()

print("### Senaste 3 discoveries")
for d in recent:
    ts = d.get('ts', '?')[:10]
    topic = d.get('topic', '?')
    content = d.get('content', '')
    # Truncate to ~120 chars for compactness
    if len(content) > 120:
        content = content[:117] + "..."
    print(f"- [{topic}] {content}")
print()

if warnings:
    print("### Aktiva varningar")
    for w in warnings[:3]:
        if len(w) > 100:
            w = w[:97] + "..."
        print(f"- {w}")
    print()

if next_items:
    print("### Nästa steg")
    for item in next_items[:3]:
        if len(item) > 100:
            item = item[:97] + "..."
        print(f"- {item}")
    print()

print(f"_Brief genererad: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC_")
PYEOF

unset _ULTIMA_DISC _ULTIMA_PROJ _ULTIMA_GUARD _ULTIMA_HANDOFF
