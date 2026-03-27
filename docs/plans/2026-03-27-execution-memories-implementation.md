# Execution Memories Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a first-class `vault/memories/execution/` layer with the initial paired execution-memory set, and document it in the Vault index.

**Architecture:** Create a new canonical memory directory for execution behavior, add four paired memory files using one shared structure, then update `vault/INDEX.md` so the new layer is discoverable and consistent with the rest of Buildr's memory model.

**Tech Stack:** Markdown content, Vault index documentation, light structural verification

---

## Task 1: Create the execution memory directory and first file

### Task 1 Files

- Create: `vault/memories/execution/builder-evaluator-memories.md`
- Verify: `vault/memories/universal-scars.md`
- Verify: `vault/memories/universal-insights.md`

### Task 1 Step 1: Write the first paired execution-memory file

Create `vault/memories/execution/builder-evaluator-memories.md` with these sections:

```md
# Memory: Builder-Evaluator Loop

## When this memory applies
Builder/evaluator waves, advisory review loops, critique-driven iteration

## Scar
...

## Why it failed
...

## Insight
...

## Repeat this pattern
...

## Signals to watch for
...

## What good looks like
...
```

Content should focus on:

- builder self-praise
- vague evaluator feedback
- ignoring evaluator input without reason
- evaluator as advisory but operationally important

### Task 1 Step 2: Review it against the design rules

Check:

- agnostic
- self-contained
- paired
- actionable during execution

Expected: No project-specific names, no stack-specific advice unless directly about execution behavior.

---

## Task 2: Add handoff and QA execution memories

### Task 2 Files

- Create: `vault/memories/execution/wave-handoff-memories.md`
- Create: `vault/memories/execution/qa-regression-memories.md`
- Verify: `vault/routines/wave-handoff.md`
- Verify: `vault/routines/post-module-qa.md`

### Task 2 Step 1: Write `wave-handoff-memories.md`

Focus on:

- missing context in handoffs
- unfinished state hidden behind optimistic summaries
- the minimum needed for another agent to continue cleanly

### Task 2 Step 2: Write `qa-regression-memories.md`

Focus on:

- shallow QA
- “looks done” vs “is verified”
- regressions introduced by later waves
- missing browser/user-flow checks where relevant

### Task 2 Step 3: Cross-check both files for overlap

Expected:

- handoff file focuses on transfer quality
- QA file focuses on verification depth
- no duplicate bullets with different wording

---

## Task 3: Add drift and rework execution memory

### Task 3 Files

- Create: `vault/memories/execution/rework-drift-memories.md`
- Verify: `vault/strategies/error-vs-feature.md`
- Verify: `vault/routines/retrospective.md`

### Task 3 Step 1: Write `rework-drift-memories.md`

Focus on:

- polishing the wrong thing
- losing the spec
- scope drift disguised as improvement
- repeated rewrites without a better contract

### Task 3 Step 2: Check distinction from the other execution memories

Expected:

- builder/evaluator file = critique loop quality
- handoff file = transfer quality
- QA/regression file = verification quality
- rework/drift file = execution control and scope discipline

---

## Task 4: Update the Vault index

### Task 4 Files

- Modify: `vault/INDEX.md`
- Verify: `docs/plans/2026-03-27-execution-memories-design.md`

### Task 4 Step 1: Add the new memory entries

Update the `## Memories` section to include:

```md
| `execution/builder-evaluator-memories` | Builder/evaluator execution loops |
| `execution/wave-handoff-memories` | Session and wave handoffs |
| `execution/qa-regression-memories` | QA depth and regression prevention |
| `execution/rework-drift-memories` | Scope drift, rework loops, execution control |
```

### Task 4 Step 2: Update the memory count

Increase the total memory count to reflect the new files.

### Task 4 Step 3: Review index wording

Expected:

- the new execution layer reads as first-class, not miscellaneous
- names match actual file paths

---

## Task 5: Run structural verification

### Task 5 Files

- Verify: `vault/memories/execution/*.md`
- Verify: `vault/INDEX.md`

### Task 5 Step 1: Read all four execution-memory files

Check:

- identical section shape
- agnostic wording
- no hidden dependencies on other files

### Task 5 Step 2: Verify the index

Check:

- all new files listed
- count updated
- descriptions accurate

### Task 5 Step 3: Run lints/diagnostics if available

Suggested verification:

```bash
python -m py_compile engines/forge_engine.py engines/bridge.py
```

This is only a regression sanity check; no engine changes are required for this plan unless documentation work reveals an unexpected dependency.

Expected: No new linter or formatting problems in changed files.

---

## Task 6: Optional follow-up plan stub

### Task 6 Files

- Reference only: `docs/plans/2026-03-27-execution-memories-design.md`

### Task 6 Step 1: Record the next follow-up target

If implementation completes cleanly, the next plan should cover one of:

- execution-memory selection wiring
- additional execution memories
- scenario-system design

Expected: follow-up is explicit, but not implemented as part of this plan.
