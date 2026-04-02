# Strategy: Parallel Wave Execution

## When to Apply
Multiple waves in the same parallel phase have no dependencies on each other and can run concurrently.

## The Approach

### Step 1: Check parallel_phases in orchestration.yaml
Read `state/orchestration.yaml` → `parallel_phases`. Phases with 2+ modules can run in parallel.

### Step 2: Verify independence
For each pair of waves in the same phase:
If [they share no files in files_to_create] → safe to parallelize.
If [they both write to the same file] → run sequentially or split the file into two.
If [one reads the other's output] → run sequentially (dependency missed in graph).

### Step 3: Assign agents/vendors
Each parallel wave gets one agent or terminal:
- Claude Code: use Agent tool to spawn sub-agents (one per wave).
- Codex/Gemini: open separate terminal sessions (one per wave).
- Mixed: assign different vendors to different waves for max throughput.

### Step 4: Merge
After all parallel waves complete:
- Update orchestration.yaml (mark all as complete).
- Verify no file conflicts (two waves writing the same file).
- Run Gate 2 for each wave independently.
- Proceed to next phase.

## Traps to Avoid
- Parallelizing waves that share state files (e.g., both append to MEMORY.md) — use locks or sequential append.
- Updating orchestration.yaml simultaneously from two agents — one agent should own the state file update, or use sequential YAML appends.
