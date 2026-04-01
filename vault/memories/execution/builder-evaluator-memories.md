# Memory: Builder-Evaluator Loop

## When this memory applies

Builder/evaluator waves, advisory review loops, critique-driven iteration, or any run where one role produces and another reviews without blocking merge by default.

## Scar

The builder treats green checks and self-review as sufficient. The evaluator either nods along or gives praise-shaped noise (“looks good”, “nice work”) without pointing at concrete risks. Feedback that does land is ignored while the builder moves to the next task, or is dismissed without a short written rationale. The loop exists on paper but does not change behavior wave to wave.

## Why it failed

Without a real contrast between build and critique, the system collapses to a single biased voice. Vague approval does not compress uncertainty. Ignoring critique without recording why erases the only independent signal in the loop. The evaluator’s advisory role was mistaken for optional etiquette instead of operational input that should routinely reshape the next build step.

## Insight

Treat evaluator output as default input for the next builder actions unless you explicitly document why not. Ask for or produce feedback that is specific: what changed, what to verify, what would change the verdict. Separate “ship anyway” from “no issues found” — advisory still means the critique is weighed, recorded, and either acted on or declined with cause.

## Repeat this pattern

- After each evaluator pass, map each finding to: fix now, defer with ticket/state note, or reject with one-line reason.
- Prefer feedback that cites observable behavior, files, or criteria — not tone.
- End the builder pass with a short delta list: what the evaluator asked for and what you did about each item.
- Keep the evaluator from blocking by default, but make non-empty evaluation the norm for non-trivial output.

## Signals to watch for

- Builder prose that sells the solution instead of listing tradeoffs and open risks.
- Evaluator notes with no failing or “watch” items on real complexity.
- Skipping the evaluation artifact or reusing stale evaluation text unchanged.
- “We’re advisory” used to mean no standard prompt for the evaluator at all.

## What good looks like

Evaluation points at concrete gaps, strengths, and ordered next checks. The builder’s follow-up shows a clear before/after against that list. Both roles assume the loop will run again — quality is cumulative, not a one-shot sign-off.
