#!/usr/bin/env bash
# auto-discovery.sh — Mine git commits for discoveries (0 tokens)
#
# Reads the last discovery timestamp from discoveries.jsonl, then uses
# `git log --since` to find all commits since. Each new commit becomes
# a discovery with session="auto-git", engine="git".
#
# Idempotent: skips commits whose hash already exists in discoveries.jsonl.
#
# Usage:
#   auto-discovery.sh                # Mine new commits since last discovery
#   auto-discovery.sh --since DATE   # Override start date (ISO 8601)
#   auto-discovery.sh --dry-run      # Show what would be written
#
# Output: Number of new discoveries written (to stderr). JSON lines to stdout.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$ULTIMA_ROOT/.." && pwd)"
DISCOVERIES="$ULTIMA_ROOT/continuum/discoveries.jsonl"

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

# --- Parse args ---
SINCE_OVERRIDE=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since)   SINCE_OVERRIDE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      echo "Usage: auto-discovery.sh [--since DATE] [--dry-run]" >&2
      exit 1
      ;;
  esac
done

# --- Find git root ---
GIT_ROOT=""
if git -C "$WORKSPACE_ROOT" rev-parse --show-toplevel &>/dev/null; then
  GIT_ROOT=$(git -C "$WORKSPACE_ROOT" rev-parse --show-toplevel)
else
  echo "WARNING: Not a git repository, nothing to mine" >&2
  exit 0
fi

# --- Determine since-date ---
SINCE_DATE="$SINCE_OVERRIDE"
if [[ -z "$SINCE_DATE" ]]; then
  # Read last discovery timestamp from discoveries.jsonl
  if [[ -f "$DISCOVERIES" && -s "$DISCOVERIES" ]]; then
    SINCE_DATE=$(tail -1 "$DISCOVERIES" | "$PYTHON_CMD" -c "
import sys, json
try:
    d = json.loads(sys.stdin.read().strip())
    print(d.get('ts', '2020-01-01T00:00:00Z'))
except:
    print('2020-01-01T00:00:00Z')
" 2>/dev/null) || SINCE_DATE="2020-01-01T00:00:00Z"
  else
    SINCE_DATE="2020-01-01T00:00:00Z"
  fi
fi

# --- Collect existing commit hashes for idempotency ---
EXISTING_HASHES=""
if [[ -f "$DISCOVERIES" && -s "$DISCOVERIES" ]]; then
  EXISTING_HASHES=$(grep -oE '"commit"[[:space:]]*:[[:space:]]*"[a-f0-9]+"' "$DISCOVERIES" 2>/dev/null | grep -oE '[a-f0-9]{7,}' || true)
fi

# --- Get commits since last discovery ---
# Format: hash|ISO-date|subject
COMMITS=$(git -C "$GIT_ROOT" log --since="$SINCE_DATE" --format="%H|%aI|%s" --reverse 2>/dev/null || true)

if [[ -z "$COMMITS" ]]; then
  echo "No new commits since $SINCE_DATE" >&2
  exit 0
fi

# --- Topic keyword map ---
# Pass commits via env var (can't pipe + heredoc simultaneously)
export _ULTIMA_DISC="$DISCOVERIES"
export _ULTIMA_DRY_RUN="$DRY_RUN"
export _ULTIMA_GIT_ROOT="$GIT_ROOT"
export _ULTIMA_EXISTING="$EXISTING_HASHES"
export _ULTIMA_COMMITS="$COMMITS"

"$PYTHON_CMD" << 'PYEOF'
import sys, json, os, subprocess
from datetime import datetime, timezone

discoveries_path = os.environ['_ULTIMA_DISC']
dry_run = os.environ['_ULTIMA_DRY_RUN'] == 'true'
git_root = os.environ['_ULTIMA_GIT_ROOT']
existing_set = set(os.environ['_ULTIMA_EXISTING'].split())
commits_raw = os.environ.get('_ULTIMA_COMMITS', '')

# Keyword → topic mapping, ordered by priority (most specific first)
# Tuples: (keyword, topic) — checked in order, first match wins
TOPIC_RULES = [
    # High-specificity keywords first
    ('hotfix', 'bugfix'), ('bugfix', 'bugfix'),
    ('readme', 'documentation'), ('documentation', 'documentation'), ('doc', 'documentation'),
    ('refactor', 'refactor'),
    ('scenario', 'scenario'), ('integration', 'scenario'),
    ('security', 'security'), ('auth', 'security'), ('permission', 'security'),
    ('architect', 'architecture'), ('design', 'architecture'), ('structure', 'architecture'),
    ('context', 'context-engineering'), ('memory', 'context-engineering'),
    ('identity', 'identity-layer'), ('route', 'model-router'),
    ('quality', 'self-validation'), ('gate', 'self-validation'),
    ('session', 'self-validation'),
    ('review', 'code-review'), ('audit', 'code-review'),
    ('perf', 'performance'), ('optim', 'performance'), ('speed', 'performance'), ('cache', 'performance'),
    ('upgrade', 'devops'), ('deploy', 'devops'), ('ci', 'devops'), ('docker', 'devops'), ('config', 'devops'), ('batch', 'devops'),
    ('test', 'testing'), ('spec', 'testing'),
    # Generic action verbs last (catch-all)
    ('fix', 'bugfix'), ('bug', 'bugfix'), ('patch', 'bugfix'),
    ('implement', 'feature'), ('create', 'feature'), ('build', 'feature'),
    ('clean', 'refactor'), ('rename', 'refactor'), ('move', 'refactor'), ('extract', 'refactor'),
    ('add', 'feature'), ('new', 'feature'),
    ('comment', 'documentation'),
]

def classify_topic(message):
    msg_lower = message.lower()
    for keyword, topic in TOPIC_RULES:
        if keyword in msg_lower:
            return topic
    return 'general'

def get_changed_files(commit_hash):
    try:
        result = subprocess.run(
            ['git', '-C', git_root, 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash],
            capture_output=True, text=True, timeout=10
        )
        files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        return files[:10]  # Cap at 10 files
    except:
        return []

new_count = 0
lines_to_write = []

for line in commits_raw.split('\n'):
    line = line.strip()
    if not line:
        continue
    parts = line.split('|', 2)
    if len(parts) < 3:
        continue

    commit_hash, commit_date, message = parts

    # Idempotency: skip if hash already in discoveries
    # Check full hash, 12-char, and 7-char prefixes
    if commit_hash in existing_set:
        continue
    if commit_hash[:12] in existing_set:
        continue
    if commit_hash[:7] in existing_set:
        continue

    topic = classify_topic(message)
    changed_files = get_changed_files(commit_hash)

    discovery = {
        'ts': commit_date,
        'session': 'auto-git',
        'engine': 'git',
        'topic': topic,
        'content': message,
        'artifacts': changed_files,
        'project': 'ultima-claw',
        'commit': commit_hash[:12]
    }

    json_line = json.dumps(discovery, ensure_ascii=False)
    print(json_line)
    lines_to_write.append(json_line)
    new_count += 1

if not dry_run and lines_to_write:
    os.makedirs(os.path.dirname(discoveries_path), exist_ok=True)
    with open(discoveries_path, 'a', encoding='utf-8') as f:
        for jl in lines_to_write:
            f.write(jl + '\n')

action = "would write" if dry_run else "wrote"
print(f"auto-discovery: {action} {new_count} discoveries from git commits", file=sys.stderr)
PYEOF

unset _ULTIMA_DISC _ULTIMA_DRY_RUN _ULTIMA_GIT_ROOT _ULTIMA_EXISTING _ULTIMA_COMMITS
