# Executor Architecture Reference

## Executor vs Operator

| Dimension | Operator | Executor |
|-----------|----------|----------|
| Input | Human description | Existing workspace |
| Output | Workspace (plans, state, contracts) | Completed project (code, assets, tests) |
| Decision-making | High — derives architecture from scratch | Low — executes pre-made decisions |
| Vault usage | Selection (which vault items to load) | Application (follow what's loaded) |
| Memory | Generates MEMORY.md | Reads + appends to MEMORY.md |
| Contracts | Generates contracts/ | Enforces and updates contracts/ |

## Executor vs Scout

The Scout brings in new knowledge; the Executor uses existing knowledge to build.
If the Executor encounters a knowledge gap, it stops and can trigger a Scout run —
it does NOT research inline during execution (that breaks the execution loop).

## State Machine

```
WORKSPACE_READY
    ↓ Phase 0: Context Load
CONTEXT_LOADED
    ↓ Phase 1: Wave Intake
WAVE_ACTIVE
    ↓ Phase 2: Module Loop (repeats per module)
MODULES_COMPLETE
    ↓ Phase 3: Quality Gate
QUALITY_PASSED
    ↓ Phase 4: Wave Completion
WAVE_COMPLETE
    ↓ Phase 5: Next Wave Selection
    → WAVE_ACTIVE (next wave)
    → COMPLETE (all waves done)
```

## Failure States

```
CONTEXT_LOAD_FAILED → Missing workspace files. Run buildr-operator first.
DEPENDENCY_UNMET    → Previous wave incomplete. Resolve before continuing.
MODULE_FAILED       → Fix or escalate. Do not skip.
CONTRACT_CONFLICT   → Update contract explicitly. Never silently break.
QUALITY_GATE_FAILED → Fix all failures. Never override the gate.
```

## Files the Executor Reads

| File | Phase | Purpose |
|------|-------|---------|
| WORKSPACE.md | 0 | Structure overview |
| AGENT.md | 0 | Behavioral protocol |
| state/orchestration.yaml | 0, 2, 4, 5 | Current state (read + write) |
| MEMORY.md | 0, 4 | Behavioral context (read + append) |
| waves/[active].md | 1 | Wave specification |
| contracts/[module].md | 1, 2 | Interface contracts |
| vault-selection/[wave].json | 1 | Pre-selected vault items |
| vault/[items] | 2 | Applied during module execution |

## Files the Executor Writes

| File | When |
|------|------|
| state/orchestration.yaml | After every module, after every wave |
| MEMORY.md | After every wave (append scars/insights) |
| contracts/[module].md | Only when contract requires version bump |
| Project source files | During module execution |
