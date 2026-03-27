# CODEX TASK: Adapt Ultima Memory Tools → Buildr memory-system/

> Read this ENTIRE file before changing anything.
> Every file listed below has exact instructions: what to keep, what to change, where it goes.

---

## Context

We have a set of bash tools from a project called "Ultima" (a session-based memory system for AI agents). We need to adapt them into Buildr's architecture. The tools are production-quality and well-tested — the adaptation is mostly renaming paths and adjusting directory references.

**Source:** The original `.sh` files (currently in the repo root or uploaded files)
**Destination:** `memory-system/tools/` within the Buildr repo

---

## Target Directory Structure

Create this EXACT structure:

```
memory-system/
├── README.md                          ← NEW (write from spec below)
├── tools/
│   ├── _common.sh                     ← ADAPT from _common.sh
│   ├── wave-start.sh                  ← ADAPT from session-start.sh
│   ├── wave-end.sh                    ← ADAPT from session-end.sh
│   ├── discovery-write.sh             ← ADAPT from continuum-write.sh
│   ├── discovery-distill.sh           ← ADAPT from distill-discoveries.sh
│   ├── discovery-mine.sh              ← ADAPT from auto-discovery.sh
│   ├── context-load.sh                ← ADAPT from context-load.sh (smallest changes)
│   ├── memory-inject.sh               ← ADAPT from inject-context.sh
│   ├── wave-brief.sh                  ← ADAPT from session-brief.sh
│   ├── wave-handoff.sh                ← ADAPT from session-handoff.sh
│   ├── wave-track.sh                  ← ADAPT from session-track.sh
│   ├── checkpoint.sh                  ← ADAPT from checkpoint.sh (minor changes)
│   └── doctor.sh                      ← ADAPT from doctor.sh
├── continuum/
│   ├── discoveries.jsonl              ← EMPTY (touch, 0 bytes)
│   ├── sessions/                      ← EMPTY DIR
│   └── checkpoints/                   ← EMPTY DIR
├── context/                           ← EMPTY DIR (generated files land here)
└── manifest.md                        ← NEW (write from spec below)
```

---

## Global Search-Replace Rules (apply to ALL .sh files)

These replacements apply to EVERY adapted file. Do them FIRST, then apply per-file changes.

| Find | Replace | Why |
|------|---------|-----|
| `ULTIMA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"` | `MEMORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"` | Rename root variable |
| `$ULTIMA_ROOT` | `$MEMORY_ROOT` | All references |
| `${ULTIMA_ROOT}` | `${MEMORY_ROOT}` | All references |
| `_ULTIMA_` | `_BUILDR_` | All env var prefixes |
| `"ultima-claw"` | `"buildr"` | Default project name |
| `.ultima/` | `memory-system/` | Path references in comments/help text |
| `CLAUDE.md` (as injection target) | `MEMORY.md` | Buildr uses MEMORY.md, not CLAUDE.md |
| `continuum-write.sh` | `discovery-write.sh` | Tool rename |
| `auto-discovery.sh` | `discovery-mine.sh` | Tool rename |
| `distill-discoveries.sh` | `discovery-distill.sh` | Tool rename |
| `inject-context.sh` | `memory-inject.sh` | Tool rename |
| `session-brief.sh` | `wave-brief.sh` | Tool rename |
| `session-handoff.sh` | `wave-handoff.sh` | Tool rename |
| `session-start.sh` | `wave-start.sh` | Tool rename |
| `session-end.sh` | `wave-end.sh` | Tool rename |
| `session-track.sh` | `wave-track.sh` | Tool rename |
| `"session"` (in JSON field names) | Keep as `"session"` | Do NOT rename JSON fields — they are part of the schema |

**IMPORTANT:** The JSON schema fields (`"session"`, `"engine"`, `"topic"`, `"content"`, `"ts"`, `"artifacts"`, `"project"`) must NOT be renamed. Only file names, directory names, and bash variable names change.

---

## Per-File Adaptation Instructions

### 1. `_common.sh` → `memory-system/tools/_common.sh`

**Changes:**
- Apply global replacements only
- In `read_arg()`: change `$_ULTIMA_ROOT` → `$_MEMORY_ROOT`, change `args/defaults.yaml` → `config/defaults.yaml`
- No other changes needed

---

### 2. `session-start.sh` → `memory-system/tools/wave-start.sh`

**Changes:**
- Apply global replacements
- Rename all internal references: `session-start` → `wave-start` in comments and echo statements
- The `--engine` flag: keep as-is (it refers to which LLM engine, not a Buildr engine)
- Change step comments:
  - "Step 1: Auto-discovery" → "Step 1: Mine git commits"
  - "Step 2: Start session tracking" → "Step 2: Start wave tracking"
  - "Step 3: Quick health check" → "Step 3: Health check"
  - "Step 4: Load context" → "Step 4: Load context"
- In the final `exec` line: `context-load.sh` keeps its name (same filename in new location)

---

### 3. `session-end.sh` → `memory-system/tools/wave-end.sh`

**Changes:**
- Apply global replacements
- Rename step comments to use "wave" instead of "session"
- Change: `session-handoff.sh` → `wave-handoff.sh`
- Change: `session-brief.sh` → `wave-brief.sh`
- Change: `session-track.sh` → `wave-track.sh`
- Change: `distill-discoveries.sh` → `discovery-distill.sh`
- Change: `inject-context.sh` → `memory-inject.sh`
- Change: `auto-discovery.sh` → `discovery-mine.sh`
- Change: `checkpoint.sh` stays `checkpoint.sh`
- Change injection target: `CLAUDE_MD="$MEMORY_ROOT/../CLAUDE.md"` → `MEMORY_MD="$MEMORY_ROOT/../MEMORY.md"`
- The `--skip-inject` flag: keep as-is

---

### 4. `continuum-write.sh` → `memory-system/tools/discovery-write.sh`

**Changes:**
- Apply global replacements
- Change: `DISCOVERIES="$MEMORY_ROOT/continuum/discoveries.jsonl"` (already correct after global replace)
- Change: default project from `"ultima-claw"` → `"buildr"`
- Change: config path from `config/defaults.json` → `config/defaults.json` (same relative path, just different root)
- The engine whitelist: add `"codex"` to the default fallback list: `WHITELIST="claude gemini codex sonnet"`
- Everything else stays identical — the secret guardrails, JSON escaping, validation are all correct as-is

---

### 5. `distill-discoveries.sh` → `memory-system/tools/discovery-distill.sh`

**Changes:**
- Apply global replacements
- In the Python section: change `os.environ['_ULTIMA_DISC']` → `os.environ['_BUILDR_DISC']` (covered by global replace)
- Change `os.environ['_ULTIMA_DEFAULTS']` → `os.environ['_BUILDR_DEFAULTS']`
- Change `os.environ['_ULTIMA_MAX']` → `os.environ['_BUILDR_MAX']`
- Change `os.environ['_ULTIMA_MAX_TOTAL']` → `os.environ['_BUILDR_MAX_TOTAL']`
- The topic weights config path stays the same relative path (config/defaults.json)
- The decay/weighting algorithm: keep EXACTLY as-is — it's production-quality

---

### 6. `auto-discovery.sh` → `memory-system/tools/discovery-mine.sh`

**Changes:**
- Apply global replacements
- Change: `_ULTIMA_DISC` → `_BUILDR_DISC`, `_ULTIMA_DRY_RUN` → `_BUILDR_DRY_RUN`, etc. (all env vars)
- Change: `_ULTIMA_GIT_ROOT` → `_BUILDR_GIT_ROOT`
- Change: `_ULTIMA_EXISTING` → `_BUILDR_EXISTING`
- Change: `_ULTIMA_COMMITS` → `_BUILDR_COMMITS`
- Change default project: `'ultima-claw'` → `'buildr'` in the Python TOPIC_RULES section
- The TOPIC_RULES keyword→topic mapping: ADD these Buildr-specific entries at the TOP of the list (before existing entries):
  ```python
  ('vault', 'vault-management'),
  ('skill', 'vault-management'),
  ('constraint', 'vault-management'),
  ('memory', 'memory-system'),
  ('imperfektum', 'memory-system'),
  ('forge', 'forge'),
  ('onboarding', 'forge'),
  ('scaffold', 'forge'),
  ('wave', 'orchestration'),
  ('orchestrat', 'orchestration'),
  ('pipeline', 'orchestration'),
  ```
- Everything else (git log parsing, idempotency, file detection): keep as-is

---

### 7. `context-load.sh` → `memory-system/tools/context-load.sh`

**Changes:**
- Apply global replacements
- Change: `IDENTITY_DIR="$MEMORY_ROOT/identity"` → REMOVE identity dir references. Buildr doesn't have SOUL.md/USER.md/AGENTS.md
- Instead, the "identity" tier loads: `$MEMORY_ROOT/../BUILDR_ARCHITECTURE.md` (the system design doc)
- Change hot tier to load:
  1. Wave brief (`context/wave-brief.md`)
  2. Current state (`../state/orchestration.yaml` if it exists, or `templates/state/orchestration.yaml`)
- Change warm tier to load:
  1. Hot tier content
  2. Handoff (`context/handoff.md`)
  3. Distilled discoveries (`context/distilled.md`)
  4. Current MEMORY.md (`../MEMORY.md`)
- Change cold tier to load:
  1. Warm tier content
  2. Full raw discoveries (`continuum/discoveries.jsonl`)
  3. Vault index (`../vault/INDEX.md`)
- Remove: All references to `SOUL.md`, `USER.md`, `AGENTS.md` — these don't exist in Buildr
- Remove: The `--reflect` mode (requires an LLM call — not appropriate for a bash tool in Buildr)
- Keep: `--budget` mode, `--refresh` mode, `--json` mode, auto-tier selection logic
- Keep: The budget/knapsack algorithm — it's excellent
- Change auto-tier thresholds: keep the same hours (2h hot, 168h warm boundary)

**This is the largest adaptation.** Take extra care with the Python embedded blocks — they reference env vars that must all be renamed from `_ULTIMA_*` to `_BUILDR_*`.

---

### 8. `inject-context.sh` → `memory-system/tools/memory-inject.sh`

**Changes:**
- Apply global replacements
- Change: default target from `"$WORKSPACE_ROOT/CLAUDE.md"` → `"$MEMORY_ROOT/../MEMORY.md"`
- Change: marker strings from `<!-- MEMORY-INJECT-START -->` → `<!-- BUILDR-INJECT-START -->`
- Change: marker strings from `<!-- MEMORY-INJECT-END -->` → `<!-- BUILDR-INJECT-END -->`
- Change: section header from `"## Continuum — Senaste discoveries"` → `"## Recent Discoveries (auto-injected)"`
- Change: the fallback insertion point from `"^## Referenser"` → `"^## How to Use This Memory"` (MEMORY.md's section)
- Keep: the tier logic (hot=3 entries, warm=distilled, cold=all raw)

---

### 9. `session-brief.sh` → `memory-system/tools/wave-brief.sh`

**Changes:**
- Apply global replacements (all env vars)
- Change: `PROJECT_MD` search candidates:
  - Replace `"$WORKSPACE_ROOT/PROJECT.md"` → keep (same location)
  - Remove `.openclaw/workspace/projects/` candidates
  - Add: `"$MEMORY_ROOT/../PROJECT.md"` as first candidate
- Change: `GUARDRAILS` path from `"$MEMORY_ROOT/skills/_guardrails.md"` → `"$MEMORY_ROOT/../vault/constraints/security.md"` (closest Buildr equivalent)
- Change: output file from `context/session-brief.md` → `context/wave-brief.md`
- In Python section: change all `os.environ['_ULTIMA_*']` → `os.environ['_BUILDR_*']`
- Change: heading from `"### Status"` → `"### Wave Status"` in output
- Change: `"### Senaste 3 discoveries"` → `"### Latest 3 Discoveries"`
- Change: `"### Aktiva varningar"` → `"### Active Warnings"`
- Change: `"### Nästa steg"` → `"### Next Steps"`
- The staleness check on handoff: keep as-is, the logic is correct

---

### 10. `session-handoff.sh` → `memory-system/tools/wave-handoff.sh`

**Changes:**
- Apply global replacements
- Change: output file from `handoff.md` → keep as `handoff.md` in `context/`
- In Python output section, change Swedish labels to English:
  - `"## Sammanfattning"` → `"## Summary"`
  - `"## Discoveries denna session"` → `"## Discoveries This Wave"`
  - `"## Ändrade filer"` → `"## Changed Files"`
  - `"## Nästa steg"` → `"## Next Steps"`
  - `"## Kontext"` → `"## Context"`
  - `"Totalt discoveries"` → `"Total discoveries"`
  - `"Denna session"` → `"This wave"`
  - `"Nästa session: börja med..."` → `"Next wave: run \`context-load.sh --tier warm\` to load this handoff."`
- Change: `"# Session Handoff: {session}"` → `"# Wave Handoff: {session}"`
- Keep: the git diff integration, discovery filtering by session ID

---

### 11. `session-track.sh` → `memory-system/tools/wave-track.sh`

**Changes:**
- Apply global replacements
- Change: session file location from `continuum/sessions/` → keep (same path)
- Change: JSON field output — keep `"id"`, `"started"`, `"ended"`, `"engine"` fields as-is
- Change: console messages from `"session-track:"` → `"wave-track:"`
- In `--start`: the sequence numbering and date logic — keep exactly as-is
- In `--end`: the discovery counting and commit counting — keep exactly as-is
- Add to the `--start` JSON template: `"wave": ""` field (empty, for future wave-number tracking)
- The engine whitelist: this tool doesn't validate engine, so no change needed

---

### 12. `checkpoint.sh` → `memory-system/tools/checkpoint.sh`

**Changes:**
- Apply global replacements only
- Change: copied context files — change `session-brief.md` → `wave-brief.md` in the copy list
- The auto-threshold (10 discoveries): keep as-is
- The manifest.json format: keep as-is

---

### 13. `doctor.sh` → `memory-system/tools/doctor.sh`

**Changes:**
- Apply global replacements
- REMOVE: Section `[identity]` (checks for SOUL.md, USER.md, AGENTS.md) — these don't exist in Buildr
- ADD: Section `[vault]` — check that `$MEMORY_ROOT/../vault/INDEX.md` exists
- ADD: Section `[engines]` — check that `$MEMORY_ROOT/../engines/imperfektum_engine.py` exists
- Change: `[injection markers]` section — look in `MEMORY.md` instead of `CLAUDE.md`, and check for `<!-- BUILDR-INJECT-START -->` markers
- Change: `[tools]` section — update the tool list to match new filenames:
  ```
  discovery-write.sh context-load.sh memory-inject.sh wave-brief.sh
  discovery-distill.sh wave-handoff.sh discovery-mine.sh wave-track.sh
  checkpoint.sh wave-start.sh wave-end.sh
  ```
- Change: `[staleness]` section — keep logic, change `handoff.md` reference to match new context dir
- Change: Title from `"Ultima Memory Kit"` → `"Buildr Memory System"`
- Keep: all staleness logic, JSON validation, sessions/checkpoints checks

---

## New Files to Create

### `memory-system/README.md`

```markdown
# Buildr Memory System

Runtime memory for Buildr agents. Tracks discoveries, manages context
tiers, and enables the Imperfektum feedback loop.

## Quick Start

```bash
# Start a wave (mines git, starts tracking, loads context)
./tools/wave-start.sh

# Log a discovery during work
./tools/discovery-write.sh --session wave-1 --engine claude \
  --topic form-validation --content "Blur validation must precede submit validation"

# End a wave (handoff, distill, inject, checkpoint)
./tools/wave-end.sh --session wave-1 --summary "Built booking calendar"
```

## Tools

| Tool | Purpose |
|------|---------|
| `wave-start.sh` | One-command wave start |
| `wave-end.sh` | One-command wave end |
| `discovery-write.sh` | Log a discovery (with secret guard) |
| `discovery-distill.sh` | Compress discoveries per topic |
| `discovery-mine.sh` | Mine git commits (0 LLM tokens) |
| `context-load.sh` | Tiered context loading (hot/warm/cold) |
| `memory-inject.sh` | Inject discoveries into MEMORY.md |
| `wave-brief.sh` | Generate hot-tier brief |
| `wave-handoff.sh` | Create wave handoff contract |
| `wave-track.sh` | Track wave lifecycle |
| `checkpoint.sh` | Snapshot state to checkpoints |
| `doctor.sh` | Health check |

## The Feedback Loop

```
Wave N starts
  → Agent reads MEMORY.md (fabricated + accumulated memories)
  → Agent builds module
  → discovery-write.sh logs what worked and what didn't
  → wave-end.sh distills discoveries
  → memory-inject.sh updates MEMORY.md with real discoveries
Wave N+1 starts
  → MEMORY.md now contains REAL memories from Wave N
  → Mixed with fabricated Imperfektum memories
  → Agent behavior improves
```

After 5 waves, MEMORY.md is majority real experience.
After 5 projects, vault/memories/ are calibrated from actual builds.
```

---

### `memory-system/manifest.md`

```markdown
# Memory System Tools Manifest

| Tool | Input | Output |
|------|-------|--------|
| `discovery-write.sh` | `--session --engine --topic --content [--type --artifacts]` | JSON line in discoveries.jsonl |
| `context-load.sh` | `[--tier hot/warm/cold] [--budget N] [--refresh]` | stdout (markdown) |
| `memory-inject.sh` | discoveries.jsonl + MEMORY.md with markers | Updated MEMORY.md |
| `wave-brief.sh` | discoveries.jsonl + PROJECT.md | context/wave-brief.md |
| `discovery-distill.sh` | discoveries.jsonl | context/distilled.md |
| `wave-handoff.sh` | `--session S --summary "..."` | context/handoff.md |
| `discovery-mine.sh` | git log | JSON lines in discoveries.jsonl |
| `wave-track.sh` | `--start / --end / --list` | Session JSON in continuum/sessions/ |
| `checkpoint.sh` | `[--slug NAME] [--auto]` | Checkpoint dir with manifest |
| `wave-start.sh` | `[--tier T] [--engine E]` | Context to stdout |
| `wave-end.sh` | `--session S --summary "..."` | All artifacts updated |
| `doctor.sh` | `[--verbose]` | OK / issues with fixes |

## Rules

- Every tool does ONE job
- `set -euo pipefail` in all scripts
- All tools are chmod +x
- JSON schema fields are NEVER renamed
- Portability: Linux, macOS, Windows (Git Bash)
```

---

## Verification Checklist (run after all changes)

```bash
# 1. All files exist
ls memory-system/tools/*.sh | wc -l
# Expected: 13 (including _common.sh)

# 2. All files executable
chmod +x memory-system/tools/*.sh

# 3. No remaining ULTIMA references
grep -r "ULTIMA" memory-system/tools/ | grep -v "^Binary"
# Expected: 0 lines

# 4. No remaining .ultima/ path references
grep -r "\.ultima/" memory-system/tools/
# Expected: 0 lines

# 5. Correct root variable everywhere
grep -c "MEMORY_ROOT" memory-system/tools/*.sh
# Expected: multiple hits in every file

# 6. Doctor passes
cd your-project && bash memory-system/tools/doctor.sh --verbose
# Expected: mostly PASS (some may fail until full workspace exists)

# 7. Empty continuum files exist
test -f memory-system/continuum/discoveries.jsonl && echo "OK"
test -d memory-system/continuum/sessions && echo "OK"
test -d memory-system/continuum/checkpoints && echo "OK"
test -d memory-system/context && echo "OK"
```

---

## What NOT to Change

These things are correct as-is and must be preserved exactly:

1. **Secret guardrails** in discovery-write.sh — the regex patterns for API keys, passwords, tokens
2. **JSON escaping** in discovery-write.sh — the `json_escape()` function
3. **Decay algorithm** in discovery-distill.sh — the `topic_weight()` function with log decay
4. **Idempotency** in discovery-mine.sh — the commit-hash dedup logic
5. **Auto-tier selection** in context-load.sh — the multi-signal decision tree
6. **Staleness detection** in wave-brief.sh — the handoff age calculation
7. **Atomic file writes** in wave-track.sh — the tmpfile→mv pattern
8. **Cross-platform stat** — the `_file_mtime()` helper (GNU vs BSD stat)

These are the hardest parts to get right and they're already correct.

---

## After Codex is Done

The human should:
1. Move `memory-system/` into the Buildr repo root
2. Run `chmod +x memory-system/tools/*.sh`
3. Run `bash memory-system/tools/doctor.sh --verbose`
4. Add `<!-- BUILDR-INJECT-START -->` and `<!-- BUILDR-INJECT-END -->` markers to any MEMORY.md that should receive auto-injected discoveries
5. Test: `bash memory-system/tools/discovery-write.sh --session test-1 --engine claude --topic test --content "Testing discovery system"`
6. Verify: `cat memory-system/continuum/discoveries.jsonl` shows one line

---

## Additional Files to Create (from user's existing system — proven patterns)

### `memory-system/templates/circuit-breaker.md`

```markdown
# Circuit Breaker Log

## Rules
Any agent increments `Attempts` each time a task is sent BACK for rework.
**Attempts >= 3** → Status becomes `BLOCKED_HUMAN` → SYSTEM STOPS.
Human must intervene before work resumes.

## Active Issues

| Task ID | Agent | Attempts | Latest Error |
|---------|-------|----------|-------------|
| — | — | 0 | System initialized |

## Resolved
<!-- Move resolved issues here with resolution notes -->
```

### `memory-system/templates/known-errors.md`

```markdown
# Known Errors & Fixes

> Check here FIRST when an error occurs. Error exists? → Apply fix directly.
> Error not listed? → Debug, fix, ADD IT HERE afterward.

## Format
### [Error message / pattern]
**Context:** When this occurs
**Fix:** Exactly what to do
**Added:** [Date] by [Agent]

## Registry
<!-- Append-only. All agents contribute. Never delete entries. -->
```

### `memory-system/templates/decisions.md`

```markdown
# Architecture Decisions

> All agents MUST respect decisions here. Decisions are LOCKED once recorded.
> To change a decision: add a NEW entry that supersedes the old one with rationale.

## Format
### [Date] — [Decision Title]
**Context:** Why this decision was needed
**Choice:** What was decided
**Alternatives considered:** What was rejected and why
**Consequences:** What this enables and constrains

## Decisions
<!-- Append-only. Newest at bottom. -->
```

### Update to `discovery-write.sh`

Add a `--direction` flag (from the user's AGENT_PROTOCOL.md concept):

In the argument parsing section, add:
```bash
DIRECTION="executing"
```

In the while loop, add:
```bash
--direction) DIRECTION="$2"; shift 2 ;;
```

Add direction validation:
```bash
VALID_DIRECTIONS="planning executing reviewing debugging"
DIR_VALID=false
for _d in $VALID_DIRECTIONS; do
  [[ "$DIRECTION" == "$_d" ]] && DIR_VALID=true
done
if [[ "$DIR_VALID" != true ]]; then
  echo "ERROR: --direction must be one of: $VALID_DIRECTIONS (got: $DIRECTION)" >&2
  exit 1
fi
```

Add `"direction":"$DIRECTION"` to the JSON output line, after the `"type"` field.

This categorizes discoveries by WHEN they were noted (during planning, execution, review, or debugging) which enables smarter distillation and context loading later.
