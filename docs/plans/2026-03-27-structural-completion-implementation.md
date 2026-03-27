# Structural Completion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Buildr structurally self-consistent by wiring runtime selection through one path, aligning generated workspaces with the orchestration contract, and adding verification for selector and workspace generation behavior.

**Architecture:** Keep the external Index and internal Vault as separate concerns, but make Vault loading flow through `engines/vault_selector.py` as the canonical selector. Preserve Forge as the project derivation engine, while extending generation so the emitted workspace contains the orchestration files and naming conventions that future agents expect.

**Tech Stack:** Python standard library, markdown templates, JSON catalog, unittest

---

## Ground Rules

- This workspace is **not** a git repository right now, so commit steps are replaced by explicit checkpoints.
- Use the Python standard library test stack (`unittest`, `tempfile`, `pathlib`) instead of adding pytest or any new dependency.
- Do not add new Vault content unless required to make the runtime or tests coherent.
- Prefer minimal edits that reduce divergence instead of introducing a second parallel convention.

---

### Task 1: Create the verification scaffold for selector behavior

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_vault_selector.py`
- Test: `tests/test_vault_selector.py`

**Step 1: Write the failing selector tests**

Add tests for:

- `select_skills("booking payment flow")` includes `payment-flow.md`
- `select_skills("responsive mobile layout")` includes `responsive-layout.md`
- `select_constraints("A")` includes `security.md`
- `select_routines("C")` includes `code-complete.md`
- `select_memories(category="booking", stack="nextjs")` includes universal + category + stack memories
- `select_for_wave(...)` returns all four keys with list values

**Step 2: Run the tests to verify the current baseline**

Run:

```bash
python -m unittest tests.test_vault_selector -v
```

Expected:

- Some tests may already pass.
- At least one test should expose any mismatch between current selector behavior and the intended wave contract.

**Step 3: Make only the minimal selector-facing fixes needed for the tests to define the contract clearly**

Allowed edits:

- `engines/vault_selector.py`
- `engines/__init__.py`

Likely work:

- normalize exports
- make default behavior explicit
- ensure returned file paths are stable and testable

**Step 4: Re-run the selector tests**

Run:

```bash
python -m unittest tests.test_vault_selector -v
```

Expected:

- All selector tests pass

**Step 5: Checkpoint**

Record that selector behavior is now codified and passing.

---

### Task 2: Make Vault selection flow through one runtime path

**Files:**
- Modify: `engines/bridge.py`
- Modify: `engines/__init__.py`
- Reference: `engines/vault_selector.py`
- Test: `tests/test_vault_selector.py`

**Step 1: Write the failing bridge-facing test or assertion**

Add one bridge-oriented test case to `tests/test_vault_selector.py` or create a focused helper assertion showing that runtime code still duplicates Vault selection logic instead of delegating through the selector.

If direct bridge testing is too heavy for this task, define the expected integration contract in comments at the top of the bridge task section inside the test file.

**Step 2: Inspect bridge responsibilities and identify exactly where Vault logic is duplicated**

Target questions:

- Which parts of `bridge.py` are about external Index tools?
- Which parts are really internal Vault selection and should delegate?
- What is the smallest refactor that separates those concerns cleanly?

**Step 3: Refactor `bridge.py`**

Make these changes:

- keep `IndexResolver` focused on external tool selection from `catalog/index.json`
- import and use `select_for_wave()` for internal Vault selection
- add a bridge helper that can render or persist selected Vault items into the generated workspace in a predictable place

Do **not** collapse Index and Vault into one concept.

**Step 4: Re-run selector tests**

Run:

```bash
python -m unittest tests.test_vault_selector -v
```

Expected:

- Selector tests still pass after the refactor

**Step 5: Checkpoint**

Record that internal Vault selection now has one canonical runtime path.

---

### Task 3: Align generated workspace output with the orchestration contract

**Files:**
- Modify: `engines/forge_engine.py`
- Modify: `engines/bridge.py`
- Reference: `templates/AGENT.md`
- Reference: `templates/WORKSPACE.md`
- Reference: `templates/RUN.md`
- Reference: `templates/state/orchestration.yaml`
- Reference: `templates/waves/000-template.md`
- Reference: `templates/contracts/template.md`

**Step 1: Write the failing workspace structure test**

Create a new integration test file:

- Create: `tests/test_workspace_generation.py`

Write a failing test that generates a temporary workspace from a minimal description and asserts the presence of:

- `WORKSPACE.md`
- `PROJECT.md`
- `SYSTEM.md`
- `MEMORY.md`
- `TOOLS.md`
- `AGENT.md`
- `RUN.md`
- `state/orchestration.yaml`
- `waves/001-foundation.md`
- `contracts/`
- `modules/`
- `qa/`

**Step 2: Run the test to verify failure**

Run:

```bash
python -m unittest tests.test_workspace_generation -v
```

Expected:

- FAIL because the current scaffold does not yet emit the full orchestration structure

**Step 3: Implement the minimal generation changes**

In `engines/forge_engine.py` and `engines/bridge.py`:

- keep `RUNBOOK.md` only if it still adds value, but make `RUN.md` the canonical execution entrypoint
- create `state/`, `waves/`, and `contracts/` directories during generation
- emit `state/orchestration.yaml` with correct initial fields
- emit `waves/001-foundation.md` using the first module or a foundation wave mapping
- make sure `AGENT.md` and `WORKSPACE.md` reading order references the same canonical files

Prefer generating these directly from existing templates or template semantics rather than inventing another parallel format.

**Step 4: Re-run the workspace generation test**

Run:

```bash
python -m unittest tests.test_workspace_generation -v
```

Expected:

- PASS on workspace structure assertions

**Step 5: Checkpoint**

Record that generated workspaces now satisfy the minimum orchestration contract.

---

### Task 4: Tighten semantic consistency between templates and runtime output

**Files:**
- Modify: `templates/AGENT.md`
- Modify: `templates/WORKSPACE.md`
- Modify: `templates/RUN.md`
- Modify: `templates/state/orchestration.yaml`
- Modify: `templates/waves/000-template.md`
- Modify: `templates/contracts/template.md`
- Modify: `engines/forge_engine.py`
- Modify: `engines/bridge.py`
- Test: `tests/test_workspace_generation.py`

**Step 1: List the naming mismatches**

Check specifically for:

- `RUNBOOK.md` vs `RUN.md`
- `.orchestration/CLAUDE.md` vs generated root-level instruction files
- wave numbering and status semantics
- whether agent instructions mention files the generator does not create

**Step 2: Choose one canonical naming scheme**

Use this target:

- `RUN.md` is canonical execution entrypoint
- `WORKSPACE.md` is canonical overview
- `AGENT.md` defines reading order and restart protocol
- `state/orchestration.yaml` is the state source of truth

If `RUNBOOK.md` remains, it must be supplemental, not contradictory.

**Step 3: Apply minimal edits**

Update templates and runtime renderers so they all point to the same contract and do not contradict one another.

**Step 4: Re-run the workspace generation test**

Run:

```bash
python -m unittest tests.test_workspace_generation -v
```

Expected:

- PASS
- no assertion failures caused by mismatched filenames or missing references

**Step 5: Checkpoint**

Record that template semantics and generated semantics now match.

---

### Task 5: Verify reference integrity for future agents

**Files:**
- Modify: `MANIFEST.md`
- Modify: `vault/INDEX.md`
- Modify: `references/category-modules.md`
- Reference: `catalog/index.json`
- Reference: `engines/bridge.py`
- Reference: `engines/vault_selector.py`

**Step 1: Compare the reference files against actual runtime behavior**

Check:

- whether `MANIFEST.md` counts and descriptions are current
- whether `vault/INDEX.md` matches the real Vault inventory
- whether `references/category-modules.md` makes claims that the generator can actually support

**Step 2: Update only the parts that would mislead another agent**

Allowed changes:

- fix counts
- fix outdated descriptions
- clarify when a reference is aspirational vs currently wired

Do **not** rewrite these files into broad product docs. Keep them as reliable references.

**Step 3: Run both test files**

Run:

```bash
python -m unittest tests.test_vault_selector tests.test_workspace_generation -v
```

Expected:

- PASS

**Step 4: Manual smoke check**

Generate one sample workspace with a short script or `WorkspaceBuilder.from_description()` into a temporary directory and confirm by inspection:

- the file inventory is coherent
- the read order makes sense
- the wave/state scaffolding is present

**Step 5: Checkpoint**

Record that runtime, templates, and references now agree closely enough for agent handoff.

---

### Task 6: Prepare the repo for team-based implementation execution

**Files:**
- Modify: `docs/plans/2026-03-27-structural-completion-design.md`
- Modify: `docs/plans/2026-03-27-structural-completion-implementation.md`

**Step 1: Add a short execution note to the design or plan if needed**

Capture:

- which files are high-conflict
- which tasks can be parallelized safely later
- which verification commands every teammate must run

**Step 2: Define safe ownership boundaries**

Target split:

- one owner for tests
- one owner for runtime wiring
- one owner for templates/reference cleanup

**Step 3: Final verification run**

Run:

```bash
python -m unittest -v
```

Expected:

- all Buildr tests pass

**Step 4: Final checkpoint**

The repo is ready for an agent-team build wave because the reasoning is done,
the implementation tasks are partitionable, and the quality gates are known.

---

## Suggested Execution Topology After Planning

Use a **parallel + merge** team shape after the controller has reviewed the plan:

- Agent A: selector tests + bridge selector integration
- Agent B: workspace generation/runtime contract
- Agent C: template and reference consistency pass
- Lead: synthesis, conflict resolution, final verification

Conflict zones that should remain single-owner during execution:

- `engines/bridge.py`
- `engines/forge_engine.py`
- `tests/test_workspace_generation.py`

---

## Definition of Done

This plan is complete when:

- `python -m unittest -v` passes
- selector behavior is covered by automated tests
- generated workspaces include the orchestration files expected by the system
- templates and runtime output no longer materially contradict each other
- reference files are trustworthy enough for the next agent to continue without
  structural guesswork
