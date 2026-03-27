#!/usr/bin/env bash
# distill-discoveries.sh — Compress raw discoveries into topic summaries
#
# Reads all discoveries, groups by topic, and produces a compact summary
# per topic. This is the "warm" tier — more context than session-brief,
# but far less than reading all raw discoveries.
#
# Pattern: Raw JSONL (cold) → Distilled summary (warm) → Session brief (hot)
#
# Usage:
#   distill-discoveries.sh                              # Output to stdout
#   distill-discoveries.sh > .ultima/context/distilled.md
#   distill-discoveries.sh --max-per-topic 5            # Limit entries per topic
#   distill-discoveries.sh --max-total 20               # Cap total output lines
#
# Output: Markdown with one section per topic, sorted by recency.
# Topics with multiple entries get compressed into a single summary line.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"

# --- Defaults ---
MAX_PER_TOPIC=3
MAX_TOTAL=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-per-topic)  MAX_PER_TOPIC="$2";  shift 2 ;;
    --max-total)      MAX_TOTAL="$2";      shift 2 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ ! -f "$DISCOVERIES" ]]; then
  echo "# Distilled Discoveries"
  echo ""
  echo "_Inga discoveries att destillera._"
  exit 0
fi

# --- Common helpers ---
source "$SCRIPT_DIR/_common.sh"
PYTHON_CMD=$(resolve_python)

DISCOVERIES_W=$(winpath "$DISCOVERIES")
DEFAULTS_JSON="$ULTIMA_ROOT/config/defaults.json"
DEFAULTS_W=$(winpath "$DEFAULTS_JSON")

export _ULTIMA_DISC="$DISCOVERIES_W"
export _ULTIMA_DEFAULTS="$DEFAULTS_W"
export _ULTIMA_MAX="$MAX_PER_TOPIC"
export _ULTIMA_MAX_TOTAL="$MAX_TOTAL"

"$PYTHON_CMD" << 'PYEOF'
import json, os, math
from collections import defaultdict
from datetime import datetime, timezone

disc_path = os.environ['_ULTIMA_DISC']
max_per_topic = int(os.environ['_ULTIMA_MAX'])
max_total = int(os.environ['_ULTIMA_MAX_TOTAL'])

# Read all discoveries
entries = []
try:
    with open(disc_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
except FileNotFoundError:
    pass

if not entries:
    print("# Distilled Discoveries")
    print()
    print("_Inga discoveries._")
    exit(0)

# Group by topic
by_topic = defaultdict(list)
for e in entries:
    topic = e.get('topic', 'unknown')
    by_topic[topic].append(e)

# --- Context Decay: weight topics by recency + frequency ---
# Newer topics weigh more, but frequently referenced topics stay relevant.
# weight = frequency / (1 + log(1 + days_old))
now = datetime.now(timezone.utc)

# --- Identity-Weighted Recall ---
# Load topic weights from config (defaults.json → identity.topic_weights).
# Fallback to 1.0 for unknown topics. Config-driven so spawned children
# can have their own weights without inheriting parent's hardcoded values.
IDENTITY_WEIGHTS = {}
defaults_path = os.environ.get('_ULTIMA_DEFAULTS', '')
if defaults_path:
    try:
        with open(defaults_path, encoding='utf-8') as f:
            cfg = json.load(f)
        IDENTITY_WEIGHTS = cfg.get('identity', {}).get('topic_weights', {})
        # Remove metadata keys
        IDENTITY_WEIGHTS = {k: v for k, v in IDENTITY_WEIGHTS.items() if not k.startswith('_')}
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass  # Fallback: all weights = 1.0

def topic_weight(topic_name):
    entries = by_topic[topic_name]
    frequency = len(entries)
    # Use most recent entry's timestamp for age
    latest_ts = entries[-1].get('ts', '')[:19]
    try:
        ts_str = latest_ts.replace('Z', '+00:00')
        entry_time = datetime.fromisoformat(ts_str)
        # Ensure timezone-aware for comparison with now (UTC)
        if entry_time.tzinfo is None:
            entry_time = entry_time.replace(tzinfo=timezone.utc)
        days_old = max(0, (now - entry_time).days)
    except (ValueError, TypeError) as e:
        days_old = 30  # Unknown age -> treat as a month old
        import sys
        print(f"[debug] timestamp parse failed for topic '{topic_name}': {latest_ts!r} ({e})", file=sys.stderr)
    decay = 1.0 / (1.0 + math.log1p(days_old))
    identity_boost = IDENTITY_WEIGHTS.get(topic_name, 1.0)
    return frequency * decay * identity_boost

# Sort topics by decayed weight (highest first)
topic_order = sorted(
    by_topic.keys(),
    key=topic_weight,
    reverse=True
)

# Calculate stats
total = len(entries)
topics_count = len(by_topic)
sessions = len(set(e.get('session', '?') for e in entries))
earliest = entries[0].get('ts', '?')[:10] if entries else '?'
latest = entries[-1].get('ts', '?')[:10] if entries else '?'

print("# Distilled Discoveries")
print()
print(f"_{total} discoveries, {topics_count} topics, {sessions} sessions ({earliest} → {latest})_")
print()

lines_emitted = 0

for topic in topic_order:
    if lines_emitted >= max_total:
        remaining = len(topic_order) - topic_order.index(topic)
        print(f"_({remaining} äldre topics utelämnade — max {max_total} rader)_")
        break

    topic_entries = by_topic[topic]
    count = len(topic_entries)

    if count == 1:
        # Single entry: emit directly (no compression needed)
        e = topic_entries[0]
        content = e.get('content', '')
        if len(content) > 150:
            content = content[:147] + "..."
        session = e.get('session', '?')
        print(f"**{topic}** _[{session}]_: {content}")
        lines_emitted += 1
    else:
        # Multiple entries: compress into summary + latest entry
        # Summary: combine key facts from all entries
        all_content = ' '.join(e.get('content', '') for e in topic_entries)
        sessions_involved = sorted(set(e.get('session', '?') for e in topic_entries))

        # Take the latest entry as primary
        latest_entry = topic_entries[-1]
        latest_content = latest_entry.get('content', '')
        if len(latest_content) > 150:
            latest_content = latest_content[:147] + "..."

        print(f"**{topic}** ({count} entries, sessions: {', '.join(sessions_involved)}):")
        print(f"  Senast: {latest_content}")
        lines_emitted += 2

        # If max_per_topic > 1, show a few more
        if max_per_topic > 1 and count > 1:
            earlier = topic_entries[-(max_per_topic):][:-1]  # all except latest
            for e in earlier[-2:]:  # max 2 earlier entries
                if lines_emitted >= max_total:
                    break
                content = e.get('content', '')
                if len(content) > 120:
                    content = content[:117] + "..."
                print(f"  Tidigare: {content}")
                lines_emitted += 1

    print()
    lines_emitted += 1  # blank line

now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
print(f"_Distillerad: {now_str} UTC | {lines_emitted} rader | max {max_total}_")
PYEOF

unset _ULTIMA_DISC _ULTIMA_MAX _ULTIMA_MAX_TOTAL
