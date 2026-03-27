# Structural Completion Design

**Date:** 2026-03-27
**Status:** Approved
**Scope:** Buildr structural completion wave

---

## Goal

Turn the repository from a promising but partially disconnected system into a
coherent bootstrap runtime that another agent can point at and continue without
manually filling structural gaps.

This wave does not aim to maximize the number of vault items. It aims to
maximize execution integrity, selector correctness, template completeness, and
handoff quality.

---

## Problem Statement

The repository already contains most of the core building blocks:

- Forge generation
- Imperfektum memory generation
- A growing Vault
- Templates for orchestration
- A catalog of external tools
- A new stateless vault selector

What is still missing is structural closure:

- Some logic is duplicated between runtime components
- Some templates exist but are not fully wired into generation
- The generated workspace contract is not yet validated end-to-end
- Reference files describe the system, but are not yet guaranteed to stay in
  sync with runtime behavior
- The new selector has no verification layer

This means the system is close to useful, but not yet self-sealing.

---

## Design Principle

This wave optimizes for one outcome:

> A fresh agent should be able to read the generated workspace and continue
> deterministically, with minimal interpretation and no missing structural
> pieces.

That principle drives all decisions below.

---

## Recommended Approach

### Approach A: Structural Completion Wave

Create a focused runtime-and-verification pass that:

- makes `vault_selector.py` the canonical selector for wave-oriented vault loading
- aligns generator output with the template contract
- verifies selector and workspace generation behavior with tests
- tightens reference documents so they reflect real runtime paths

**Why this is the chosen approach**

- Highest leverage per file touched
- Converts existing work into an actually operable system
- Reduces future rework before scaling the Vault further
- Creates a clean base for later agent-team execution

### Approach B: Expand the Vault first

Add many more skills, memories, and routines before tightening runtime wiring.

**Why not now**

- Increases content volume before the system is fully closed
- Risks producing more high-quality assets that are still loaded inconsistently
- Solves quantity before integrity

### Approach C: Build a flagship demo first

Generate a heroic workspace to prove the concept.

**Why not now**

- Produces evidence, not infrastructure
- Can hide structural brittleness behind a single happy path
- Better after the runtime is more deterministic

---

## Architecture

### 1. Canonical Vault Selection

`engines/vault_selector.py` becomes the single runtime authority for choosing
wave-specific vault items.

Implications:

- `bridge.py` should delegate selection to the selector instead of maintaining a
  separate selection model for the Vault layer
- selector APIs should remain stateless and predictable
- category and stack memory selection should be consistent with Forge output

The external Index is still separate. It answers "which external tools are
relevant?" while the vault selector answers "which internal vault items should
the current wave load?"

### 2. Workspace Contract Completion

Generated workspaces should consistently include the core reading and execution
contract:

- `WORKSPACE.md`
- `PROJECT.md`
- `SYSTEM.md`
- `MEMORY.md`
- `TOOLS.md`
- `AGENT.md`
- `RUN.md`
- `state/orchestration.yaml`
- at least one wave file
- `contracts/`
- `modules/`
- `qa/`

If the runtime currently emits a mix of `RUNBOOK.md` and `RUN.md`, or uses one
set of agent instructions in templates and another in generator output, this
wave resolves the mismatch instead of preserving parallel conventions.

### 3. Reference Integrity

Repository references should act as stable orientation points, not just
documentation snapshots.

This wave treats the following files as structural references:

- `MANIFEST.md`
- `vault/INDEX.md`
- `references/category-modules.md`
- `catalog/index.json`

The goal is not to automate all of them immediately. The goal is to make sure
their claims match the runtime enough that a future agent can rely on them.

### 4. Verification Layer

Two forms of verification are required:

- selector tests
- light workspace generation tests

Selector tests prove that wave intent + tier + category + stack produce the
expected vault selections.

Workspace generation tests prove that the generated scaffold contains the files
and structural fields required by the Buildr contract.

---

## Components and Responsibilities

### `engines/vault_selector.py`

Responsibility:

- map wave intent to skill file paths
- map tier to constraints and routines
- map category and stack to memory templates

Expected outcome:

- deterministic output
- no hidden state
- easy unit testing

### `engines/bridge.py`

Responsibility:

- orchestrate Forge + Imperfektum + Index + Vault selection
- emit the final workspace package

Expected outcome:

- use the selector instead of duplicating Vault logic
- keep Index logic focused on external tools
- produce a structurally complete workspace

### `engines/forge_engine.py`

Responsibility:

- derive project structure from onboarding signals
- generate project files, module specs, QA docs

Expected outcome:

- align generated filenames and execution docs with the workspace contract used
  elsewhere
- avoid generator/template divergence

### `templates/*`

Responsibility:

- define the canonical workspace contract

Expected outcome:

- generator output should match template semantics
- naming and reading order should be consistent across templates and runtime

---

## Data Flow

Target flow for a generated workspace:

1. Human description enters Forge.
2. Forge derives category, stack, modules, and design system.
3. Bridge asks Index which external tools are relevant.
4. Bridge asks the Vault selector which internal vault items a wave should load.
5. Imperfektum generates project memory.
6. Runtime writes a workspace whose execution files use one consistent contract.
7. A fresh agent reads `WORKSPACE.md` and can continue without conversation
   history.

This wave focuses on steps 3-7.

---

## Error Handling

The structural completion wave should explicitly handle these failure modes:

- missing vault item file referenced by selector
- category or stack memory absent on disk
- mismatch between template expectations and generated filenames
- missing state defaults required by orchestration
- runtime behavior depending on reference files that are only descriptive

Handling strategy:

- tolerate absent optional files where appropriate
- fail clearly when a required structural file is missing
- keep behavior deterministic and easy to test

---

## Testing Strategy

### Unit tests

Add tests for `vault_selector.py` covering:

- skill keyword matching
- tier-based constraints
- tier-based routines
- category memories
- stack memories
- combined `select_for_wave()`

### Integration tests

Add at least one lightweight workspace generation test covering:

- workspace file inventory
- presence of state and wave scaffolding
- presence of memory and tools docs
- consistency of core read order files

### Manual verification

After code changes:

- run the relevant test suite
- inspect one generated sample workspace
- confirm the output reads like a coherent handoff target

---

## Non-Goals

This wave does not attempt to:

- finish the full 30-40 skill target
- add every remaining memory template
- create new goals in `goals/`
- design the final multi-agent runtime itself
- implement advanced wave planning for every category

Those are follow-on waves, not part of this structural closure pass.

---

## Acceptance Criteria

This design is successful when all of the following are true:

- vault selection is driven through a single clear runtime path
- generated workspaces include the core structural files expected by the system
- template naming and generator naming no longer conflict in meaningful ways
- selector behavior is covered by automated tests
- a basic workspace generation path is covered by automated verification
- reference documents no longer materially mislead a future agent

---

## Agent-Team Readiness

This design intentionally prepares the repository for a later agent-team build
phase.

The team should only be launched after:

- the implementation plan is written
- file ownership is partitioned
- conflict zones are identified
- verification commands are known

That transition belongs to the next step, not this design document.

---

## Summary

The highest-leverage move is not more content. It is structural closure.

This wave makes Buildr more trustworthy as a bootstrap system by finishing the
runtime wiring, aligning the workspace contract, and adding the first real
verification layer around the selector and generated output.
