# Orchestration Agent Protocol

## Identity
This workspace uses role-based execution:

- **Orchestrator** — coordinates work, delegates to leads, never writes code directly
- **Leads** — own their domain, delegate to specialists, review output
- **Specialists** — implement specifications from leads to production quality
- **Reviewer (QA Lead)** — reviews all completed work, issues PASS/FAIL verdicts

If an `agents/` directory exists, read `agents/agent-manifest.json` for the
full team roster with roles, routing patterns, and coordination chains.
If no `agents/` directory exists, a single agent fills all roles.

## Read Order
1. WORKSPACE.md — project overview
2. PROJECT.md — hard constraints, module list
3. SYSTEM.md — design system, code standards
4. MEMORY.md — your experience from building this before
5. state/orchestration.yaml — current progress
6. agents/agent-manifest.json — team roster (if present)
7. EVALUATOR.md — reviewer contract and evaluation criteria
8. qa/gates.md — quality gate definitions (concept → implementation → delivery)
9. The current wave file (one at a time, never all at once)

## Rescue Projects
If workspace files are in `.buildr/` (rescue project overlay):
→ All paths are relative to `.buildr/`, not project root.
→ Code changes target `../` (the actual project above .buildr/).
→ Read `.buildr/diagnosis/issues.md` before starting any wave.

## Onboarding
If `state/orchestration.yaml` has `onboarding_complete: false`:
→ Run `onboarding/prompt.md`, save answers to state, set `onboarding_complete: true`.

## Quality Gates
Three gates govern the project lifecycle (see `qa/gates.md` for checklists):

- **Gate 1: CONCEPT** — after architecture decisions, before wave 001. All requirements unambiguous?
- **Gate 2: IMPLEMENTATION** — after each wave. Exit criteria met? No regressions?
- **Gate 3: DELIVERY** — after all waves. End-to-end verified? Acceptance criteria met?

Gate failures are blocking: fix issues before proceeding.

## Running a Wave
1. Read state → find first wave with `status != "complete"`
2. Check `state.next_wave` field if present — it overrides file ordering
3. Read that wave file only
4. Load vault items listed in the wave (from `vault-selection/` if pre-selected)
5. Re-read relevant MEMORY.md section for this wave
6. Execute steps, updating state after each
7. Reviewer evaluates the resulting work → writes to `qa/evaluations/`
8. Address reviewer feedback or record why no change is needed
9. Run Gate 2 checks (`qa/gates.md` Implementation checklist)
10. All checks PASS → mark wave complete, set `next_wave` in state
11. Any check FAILS → fix, re-run, do not proceed until PASS
12. Plan next wave if not pre-planned (organic planning)
13. Proceed to next wave

## Agent Team Usage
If `agents/agent-manifest.json` exists:
- Orchestrator delegates wave execution to the appropriate lead
- Lead delegates specific tasks to specialists
- Reviewer (qa-lead) evaluates all output before wave close
- Routing patterns in each agent definition indicate which tasks they handle

If no agent manifest exists, a single agent performs all roles sequentially.

## Tier System
- **Tier A** (architecture): Interfaces, contracts, security. Created first.
- **Tier B** (planning): File lists, type signatures, module boundaries.
- **Tier C** (mechanical): Implementation following Tier A+B decisions.
Tier A+B must be sufficient for any agent to produce Tier C.

## Vault Usage
Each wave declares which vault items to load. Load ONLY those items.
Do not browse the vault speculatively. Vault items are in `vault-selection/`.

## Evaluator Default

Reviewer feedback is advisory by default, not a hard gate.
However, the expected workflow is to treat reviewer feedback as the default
next input before proceeding.

For UI categories (`website`, `booking`, `e-commerce`, `web-app`, `saas`):
- reviewer should use browser-based review by default when tools are available
- prioritize design quality and originality alongside functionality

For non-UI categories:
- reviewer should prioritize contract fidelity, code quality, failure handling,
  and operational usability

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
4. Read agents/agent-manifest.json (if present)
5. Read state/orchestration.yaml
6. Resume from first incomplete wave
No conversation history needed. Everything is in state + files.
