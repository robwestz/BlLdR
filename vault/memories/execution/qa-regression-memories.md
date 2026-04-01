# Memory: QA Depth and Regression Leaks

## When this memory applies

After modules or waves complete, before marking work done, when changing code that other features depend on, or when UI/API behavior must stay stable across iterations.

## Scar

QA becomes a quick skim: lint passes, one happy path, screenshot of the happy screen. Later waves change shared plumbing; something that worked in wave two silently breaks in wave five because nobody re-ran the earlier flows. The team conflates “no errors in the last build” with “behavior still matches acceptance criteria.”

## Why it failed

Verification depth was traded for speed without recording the trade. Regression risk grows with touch points to shared state, routing, auth, and data contracts, but checklists did not scale with that coupling. Browser or user-journey checks were treated as optional extras instead of part of the definition of done when the product has a surface users touch.

## Insight

Match verification to blast radius: if you changed it, re-verify every path that depends on it. Separate “builds” from “behaves”: run the smallest set of checks that would catch a wrong assumption, not the smallest set that feels fast. Record what was checked so the next wave can extend rather than reset.

## Repeat this pattern

- Tie each merge or wave close to explicit acceptance criteria checks, not vibes.
- After cross-cutting changes, re-run affected module checks from prior waves or document residual risk.
- For interactive surfaces, include at least one realistic flow that hits changed code — automated or manual with steps listed.
- When skipping depth, write one line: risk accepted because …

## Signals to watch for

- Test or check list that only grows never — every wave adds code but not checks.
- QA section that lists tools run but not behaviors proven.
- “Works on my machine” without commands or data prerequisites.
- Fixes that remove logging or tests to get green faster.

## What good looks like

You can point to what would have failed if the latest change broke an old promise — and that check actually ran or the gap is called out. Subsequent waves inherit a verification ladder, not amnesia.
