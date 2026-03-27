# Orchestration Agent Protocol

## Identity
This workspace uses two default roles:

- **Builder** — executes waves, implements modules, and updates state
- **Evaluator** — reviews completed work, challenges weak output, and writes advisory feedback

The builder remains the primary execution role.
The evaluator is the default critical counterweight and should be used after each completed wave or module.

## Read Order
1. WORKSPACE.md — project overview
2. PROJECT.md — hard constraints, module list
3. SYSTEM.md — design system, code standards
4. MEMORY.md — your experience from building this before
5. state/orchestration.yaml — current progress
6. EVALUATOR.md — evaluator contract and review criteria
7. The current wave file (one at a time, never all at once)

## Onboarding
If `state/orchestration.yaml` has `onboarding_complete: false`:
→ Run `onboarding/prompt.md`, save answers to state, set `onboarding_complete: true`.

## Running a Wave
1. Builder reads state → finds first wave with `status != "complete"`
2. Builder reads that wave file only
3. Builder loads vault items listed in the wave
4. Builder re-reads relevant MEMORY.md section for this wave
5. Builder executes steps, updating state after each
6. Evaluator reviews the resulting work and writes advisory feedback
7. Builder addresses evaluator feedback or records why no change is needed
8. Run QA (`qa/checklist.md` for this module)
9. All QA checks PASS → mark wave complete in state
10. Any QA check FAILS → fix, re-run QA, do not proceed until PASS
11. Plan next wave if not pre-planned (organic planning)
12. Proceed to next wave

## Tier System
- **Tier A** (architecture): Interfaces, contracts, security. Created first.
- **Tier B** (planning): File lists, type signatures, module boundaries.
- **Tier C** (mechanical): Implementation following Tier A+B decisions.
Tier A+B must be sufficient for any agent to produce Tier C.

## Vault Usage
Each wave declares which vault items to load. Load ONLY those items.
Do not browse the vault speculatively. Vault items are in `vault-selection/`.

## Evaluator Default

Evaluator feedback is advisory by default, not a hard gate.
However, the expected workflow is to treat evaluator feedback as the default next input before proceeding.

For UI categories (`website`, `booking`, `e-commerce`, `web-app`, `saas`):
- evaluator should use browser-based review by default when the tools are available
- prioritize design quality and originality alongside functionality

For non-UI categories:
- evaluator should prioritize contract fidelity, code quality, failure handling, and operational usability

## Imperfektum Protocol
Before each wave, re-read the relevant section of MEMORY.md.
The memories are real experiences. The mistakes listed there happened.
Do not repeat them. The insights listed there worked. Replicate them.

## Prohibitions
- Do NOT invent features not in PROJECT.md or onboarding answers
- Do NOT write to paths outside those declared in the current wave
- Do NOT modify contracts without bumping contract_version in state
- Do NOT skip QA after any module
- Do NOT read completed wave files (state has all decisions)
- Do NOT plan future waves during current wave execution

## Budget
`state/orchestration.yaml` tracks `loc_budget` and `loc_consumed`.
Each wave declares expected LOC consumption. Overruns require user approval.

## Restart Protocol
If context is lost (new session, compaction):
1. Read this file (CLAUDE.md)
2. Read MEMORY.md
3. Read EVALUATOR.md
4. Read state/orchestration.yaml
5. Resume from first incomplete wave
No conversation history needed. Everything is in state + files.
