# Memory: Rework, Drift, and Execution Control

## When this memory applies

Mid-wave polish, repeated refactors, “while we’re here” expansions, or when the same area is rewritten multiple times without a tighter spec.

## Scar

Energy goes into reshaping implementation details while the problem statement and contracts drift. Scope expands under the label of quality: extra features, new abstractions, or visual passes that nobody prioritized. Rework loops start — same module name, third rewrite — still without an updated contract or decision log. The build feels busy; delivery toward acceptance turns opaque.

## Why it failed

Execution control was mistaken for perfectionism. Without anchoring each iteration to a written spec or contract version, every pass invents a new implicit target. Drift dressed as improvement bypasses prioritization: the easiest work (local prettiness) crowded out the binding work (interfaces, edge cases, integration).

## Insight

Polish the right thing: the next acceptance criterion or contract — not the ego of the current file. When rewriting, bump or amend the contract first or append a short decision so the rewrite has a stable “why.” If scope changes, make it visible in backlog or state, not only in code.

## Repeat this pattern

- Before a non-trivial rewrite, state what is wrong with the current artifact in one paragraph.
- After two full passes on the same unit without clearer acceptance, stop for spec/contracts — not a third cosmetic pass.
- Label scope changes explicitly; never merge “free” behavior without intent.
- Prefer small vertical slices that meet criteria over horizontal perfection in one layer.

## Signals to watch for

- Growing file count of “v2” or “old” variants without deprecation story.
- Meetings and diffs about style while integration tests stay red or absent.
- Contract version stuck at initial while behavior diverged.
- “I’ll just fix this” chains that bypass the wave plan.

## What good looks like

Each wave produces observable progress against declared criteria. Rework is traceable to a documented gap or decision, not habit. Scope is boringly stable unless someone intentionally moves the goal — then everyone sees the move.
