# Run

Agents: execute these steps in order.

1. Read **AGENT.md** for role, reading order, and execution gates.
2. Read **EVALUATOR.md** for evaluator review criteria and output expectations.
3. Read **WORKSPACE.md** for the file contract and project summary.
4. Read `MEMORY.md` for your experience with this project.
5. Read `state/orchestration.yaml` for current progress.
6. If `onboarding_complete` is false → run `onboarding/prompt.md` (if present).
7. Find the first wave in `waves/` with status ≠ complete (per state file).
8. Load vault items declared in that wave.
9. Builder executes the wave's steps.
10. Evaluator reviews the result and writes advisory feedback in `qa/evaluations/`.
11. Builder addresses evaluator feedback or records why no change is needed.
12. Run QA (`qa/checklist.md` for this module). All checks must PASS.
13. Update `state/orchestration.yaml`. Plan the next wave if needed.
14. Repeat from step 7 until all waves complete.
15. Report summary to user.
