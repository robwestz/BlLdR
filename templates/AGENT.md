# Builder Agent Instructions

> Read this at session start and after every context compaction.

## Reading Order

| # | File | When |
|---|------|------|
| 0 | **WORKSPACE.md** | First — understand the project |
| 1 | **PROJECT.md** | Before building — hard constraints |
| 2 | **SYSTEM.md** | Before building — design + code standards |
| 3 | **MEMORY.md** | Before building — your experience from last time |
| 4 | **TOOLS.md** | Reference — available tools |
| 5 | **EVALUATOR.md** | Understand how evaluator feedback is produced and consumed |
| 6 | **RUN.md** | Execute — start the orchestration loop |
| 7 | **modules/[current]** | Per module — read before building |

## Execution Gate

Before building ANYTHING, confirm:

```
I have read WORKSPACE.md, PROJECT.md, SYSTEM.md, MEMORY.md, EVALUATOR.md, and RUN.md. I confirm:

I WILL:
  ✓ Follow RUN.md for the orchestration loop and update state/orchestration.yaml
  ✓ Build modules in order; use RUNBOOK.md only as supplemental module detail
  ✓ Read each module spec before building it
  ✓ Load vault items declared in each wave
  ✓ Hand completed wave output to the evaluator before moving on
  ✓ Treat evaluator feedback as default input for the next iteration
  ✓ Run QA after every module (all checks PASS)
  ✓ Follow the design system in SYSTEM.md exactly
  ✓ Avoid every mistake listed in MEMORY.md
  ✓ Ask when uncertain — never guess

I WILL NOT:
  ✗ Skip modules or reorder them
  ✗ Change the design system mid-build
  ✗ Write code without reading the module spec
  ✗ Ignore evaluator feedback without a concrete reason
  ✗ Proceed if QA fails
  ✗ Invent features not in PROJECT.md
```

## Per Module
1. Read the module spec
2. Load vault items for this wave
3. Re-read relevant MEMORY.md section
4. Build
5. Hand off the result to the evaluator and read the evaluation feedback
6. Apply the evaluator's recommended fixes or record why no change is needed
7. Run QA → all checks PASS
8. Update state
9. Next module

## Restart Protocol
Context lost? New session?
1. Read this file
2. Read MEMORY.md
3. Read EVALUATOR.md
4. Read state/orchestration.yaml
5. Resume from first incomplete wave
No conversation history needed.
