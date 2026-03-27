# Strategy: Error vs Feature

## When to Apply
When deciding whether to stop building features in order to fix a known bug.

## The Approach

### Step 1: Classify the Bug
- Data corruption, security vulnerability, production crash → fix immediately, no discussion.
- Wrong result, core flow broken, UX severely degraded → fix before next feature.
- Minor visual issue, edge case with workaround → log and continue.

### Step 2: Estimate Blast Radius
How many users are affected? How often does it occur?
A bug that hits 1% of users daily may outrank one that hits 50% monthly.

### Step 3: Estimate Deferral Cost
Does this bug get harder to fix the longer you wait?
Does it interact with the features currently being built?
If yes to either → fix now, not later.

## Decision Points
Fix immediately if: security risk, data loss risk, crash in production, blocks users from core flow.
Defer if: cosmetic issue, edge case, a documented workaround exists and is communicated.
Fix before next feature if: the bug will be touched by the next feature's code anyway.

## Traps to Avoid
- "It only happens sometimes": Intermittent bugs are often the most severe — they indicate unstable state.
- Deferring security bugs because they haven't been exploited yet: Exploitation is not the threshold for urgency.
- Fixing and building simultaneously: Changing code while introducing new code masks which change caused new failures.
