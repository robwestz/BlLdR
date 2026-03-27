# Run

Agents: execute these steps in order.

1. Read **CLAUDE.md** for orchestration protocol and role definitions.
2. Read **AGENT.md** for builder role and execution gates.
3. Read **EVALUATOR.md** for reviewer criteria and output expectations.
4. Read `agents/agent-manifest.json` for team roster (if present).
5. Read **WORKSPACE.md** for the file contract and project summary.
6. Read `MEMORY.md` for your experience with this project.
7. Read `state/orchestration.yaml` for current progress.
8. **Gate 1 (Concept):** If wave 001 not started → run `qa/gates.md` Concept checklist. All PASS before proceeding.
9. If `onboarding_complete` is false → run `onboarding/prompt.md` (if present).
10. Find the first wave in `waves/` with status ≠ complete (check `state.next_wave` first).
11. Load vault items declared in that wave (from `vault-selection/` or by reading vault/ directly).
12. Execute the wave's steps (delegate to specialists if agent team exists).
13. Reviewer evaluates the result → writes to `qa/evaluations/`.
14. Address reviewer feedback or record why no change is needed.
15. **Gate 2 (Implementation):** Run `qa/gates.md` Implementation checklist. All checks must PASS.
16. Update `state/orchestration.yaml`: mark wave complete, set `next_wave`.
17. Plan the next wave if not pre-planned (organic planning).
18. Repeat from step 10 until all waves complete.
19. **Gate 3 (Delivery):** Run `qa/gates.md` Delivery checklist. All checks must PASS.
20. Report summary to user.
