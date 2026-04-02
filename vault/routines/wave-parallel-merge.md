# Routine: Wave Parallel Merge

## When to Run
After all waves in a parallel phase have completed. Before proceeding to the next phase.

## Checks (binary — each passes or fails)

1. All waves in the phase have status: complete in orchestration.yaml.
2. No two waves created the same file (check files_to_create overlap).
3. No contract version conflicts (same contract bumped by two waves).
4. Project still builds without errors (`npm run build` or equivalent).
5. Each wave passed its own Gate 2 check independently.
6. orchestration.yaml is consistent (no duplicate entries, no missing waves).

## If Fails
- File conflict: decide which version to keep, merge manually, re-run QA for both waves.
- Contract conflict: bump to higher version, reconcile interfaces, re-run dependent modules.
- Build failure: identify which wave's changes break the build, fix, re-run Gate 2.

## Expected Duration
Under 2 minutes (file checks + one build).
