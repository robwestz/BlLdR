# Execution Memories Design

**Date:** 2026-03-27
**Status:** Approved
**Scope:** Buildr execution-memory expansion

---

## Goal

Add a first-class `vault/memories/execution/` layer to Buildr so generated
workspaces can inherit reusable lessons about how agents should execute work,
not just what they should build.

This design focuses on execution quality across waves, handoffs, QA, evaluator
feedback, and rework control. It does not attempt to expand every remaining
memory category at once.

---

## Problem Statement

Buildr already has useful memory layers:

- `universal-*` for all-project lessons
- `category/*` for product-type lessons
- `stack/*` for technology-specific lessons

What is still missing is a dedicated memory layer for execution behavior.

Right now, some of the highest-leverage lessons are about:

- when builders drift from the spec
- how evaluator feedback should be used
- what a complete handoff must contain
- why QA often looks complete before it actually is
- how agents get trapped in rework loops

These lessons are not specific to one category or stack. They are execution
patterns. Without a first-class place for them, they risk being duplicated,
buried in universal files, or omitted entirely from wave selection.

---

## Design Principle

Execution memories should be:

- agnostic
- self-contained
- operational during a wave, not reflective only after a wave
- selectable alongside category and stack memories

They should tell the agent both:

- what failure pattern to avoid
- what repeatable pattern to apply instead

That is why the design uses **paired memories** instead of separate
`scars`/`insights` files.

---

## Recommended Approach

### Approach A: First-Class `execution/` Memory Layer

Create a new directory:

- `vault/memories/execution/`

Each file represents an execution-domain lesson that applies across many
project types and stacks.

This is the recommended approach because it preserves a clean mental model:

- `universal` = broad lessons that apply almost everywhere
- `category` = product-shape lessons
- `stack` = technical-stack lessons
- `execution` = agent-workflow lessons

### Approach B: Fold execution memories into `universal-*`

Rejected because it mixes two different scopes:

- universal craftsmanship lessons
- specific execution-loop lessons

This makes selection and future tooling less precise.

### Approach C: Scatter execution memories across `category/` and `stack/`

Rejected because execution problems are usually orthogonal to category/stack.
This would create duplication and weaken retrieval quality.

---

## Architecture

### 1. New Canonical Directory

Add:

- `vault/memories/execution/`

This becomes the canonical home for execution-specific paired memories.

### 2. Paired Memory Format

Every execution-memory file should use the same structure:

1. `# <Title>`
2. `## When this memory applies`
3. `## Scar`
4. `## Why it failed`
5. `## Insight`
6. `## Repeat this pattern`
7. `## Signals to watch for`
8. `## What good looks like`

This format makes the file useful at runtime:

- `Scar` captures the anti-pattern
- `Insight` captures the corrective pattern
- `Signals to watch for` makes the lesson detectable mid-wave
- `What good looks like` gives builder/evaluator a target state

### 3. Initial File Set

The first execution-memory batch should contain four files:

- `vault/memories/execution/builder-evaluator-memories.md`
- `vault/memories/execution/wave-handoff-memories.md`
- `vault/memories/execution/qa-regression-memories.md`
- `vault/memories/execution/rework-drift-memories.md`

### 4. Selection Model

Execution memories should be canonical in `execution/`, but composable with the
existing layers.

Example target selection shape for a wave:

- one or more execution memories
- zero or more category memories
- zero or more stack memories

This allows a single wave to combine:

- execution discipline
- product-shape lessons
- technical-stack lessons

without creating duplicate files.

---

## Components and Responsibilities

### `vault/memories/execution/*`

Responsibility:

- encode reusable lessons about agent execution behavior
- remain agnostic and self-contained
- help builders and evaluators act better during the wave

Expected outcome:

- fewer bad handoffs
- better evaluator usage
- stronger QA depth
- less drift and rework

### `vault/INDEX.md`

Responsibility:

- list the new `execution/*` memory files clearly
- preserve the mental model of memory scopes

Expected outcome:

- future agents can discover the new layer without guessing

### Selector/runtime follow-up

Responsibility:

- later wire execution-memory selection into wave loading

Expected outcome:

- the new files become operational, not just documented

This wiring is a follow-up implementation concern and not a blocker for adding
the memory layer itself.

---

## Data Flow

Target memory composition for a wave:

1. Buildr identifies the wave type and execution risks.
2. The selector chooses one or more execution memories.
3. The selector optionally adds category and stack memories.
4. The generated workspace or runtime loads that combined memory set.
5. Builder and evaluator use the same execution memories as shared behavioral
   guardrails.

This is especially important now that Buildr workspaces use a default
builder/evaluator pattern.

---

## Error Handling

The design should prevent these failure modes:

- execution lessons hidden in unrelated memory scopes
- separate scars and insights drifting apart
- memories that describe problems but do not tell the agent what to do instead
- runtime selection logic that cannot distinguish execution lessons from other
  memory types

Mitigation:

- keep execution memories in their own directory
- keep each file paired
- use a shared file template
- keep the files fully readable in isolation

---

## Testing Strategy

### Manual verification

After the first batch is created:

- confirm all four files share the same section structure
- confirm each file is agnostic and self-contained
- confirm `vault/INDEX.md` lists them accurately
- confirm the files are distinct and not duplicate summaries of each other

### Follow-up verification

When selector/runtime wiring happens later:

- add tests that prove execution memories can be selected with category and
  stack memories in the same wave

---

## Non-Goals

This design does not attempt to:

- finish all remaining category memories
- finish all remaining stack memories
- add a scenario system yet
- add clone applications yet
- design the SDK lane yet
- redesign Imperfektum generation end-to-end

Those are follow-on tracks after execution memories are established.

---

## Acceptance Criteria

This design is successful when:

- `vault/memories/execution/` exists as a first-class area
- the first four execution-memory files exist
- all four use the paired format
- all four are agnostic and self-contained
- `vault/INDEX.md` documents the new execution-memory layer accurately
- Buildr now has a clean four-part memory model: universal, category, stack,
  execution

---

## Summary

The next highest-leverage memory expansion is not more stack or category depth.
It is a reusable execution-memory layer.

Creating `vault/memories/execution/` gives Buildr a clean place to encode how
agents should behave across handoffs, QA, evaluator feedback, and rework. That
improves every future workspace, regardless of stack or category.
