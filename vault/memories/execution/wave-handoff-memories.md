# Memory: Wave Handoffs

## When this memory applies

Session boundaries, wave boundaries, multi-agent handoffs, or any stop where someone else (or future you) must continue without re-deriving context from chat history.

## Scar

The handoff reads like a victory lap: what went well and “almost done”, while the real state hides in uncommitted files, stale orchestration fields, or mental notes. The next agent opens the workspace, sees green language, and builds on wrong assumptions — or repeats work because nobody recorded what failed and what was intentionally left open.

## Why it failed

Optimistic summaries feel faster than precise state, but they externalize cost onto the receiver. Minimum viable handoff was confused with minimum honest summary. Without file pointers, command results, and explicit next actions, continuity depends on memory that the handoff explicitly destroyed by ending the session.

## Insight

Optimize for the receiver: what must they read, run, and touch first? Lead with blocking facts — failing checks, ambiguous decisions, partial modules — then achievements. Tie claims to artifacts: paths, IDs, timestamps in state, last commands and outcomes where useful.

## Repeat this pattern

- State file: current wave, what is complete vs in progress, known blockers.
- One paragraph: “If you only do three things next, they are …”
- List open branches of work with owner or “unowned” explicitly.
- Note environment assumptions (tooling, secrets present/absent) only as facts, not stories.

## Signals to watch for

- Handoff that never mentions a failing test, TODO, or deferred acceptance criterion.
- “Read the thread” as the primary instruction.
- Orchestration or contracts out of sync with the filesystem without calling that out.
- Copy-paste of generic motivational text instead of a checklist.

## What good looks like

A new executor can pick the correct next wave step, reproduce the last known good verify step, and see why anything ugly was left ugly — without asking the prior session. The handoff ages well: it is still true after a night’s sleep.
