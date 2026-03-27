# Routine: Wave Handoff

## When to Run
Before ending any work session mid-wave, or before handing a wave to a different agent.
Also run at wave completion, before the next wave begins.

## Checklist
- [ ] `state/orchestration.yaml` reflects the exact current state: which modules are complete, which are in progress, which are not started
- [ ] Every module completed this session has a contract written or updated in `contracts/`
- [ ] `MEMORY.md` has been updated with any scars or insights from this session
- [ ] All work-in-progress code is committed or clearly staged — no orphaned changes
- [ ] Any decision made this session (tech choice, scope cut, deferred item) is recorded in `state/orchestration.yaml` under `decisions`
- [ ] The next action is written in `state/orchestration.yaml` under `next_action`: specific enough that a new agent can continue without asking questions

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not hand off until all pass.

## Duration
5 minutes.
