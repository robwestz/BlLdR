# Strategy: Scope Cutting

## When to Apply
When the budget (time, tokens, LOC) is insufficient for all planned features.

## The Approach

### Step 1: Classify every feature
Must-have: The product is broken without it.
Should-have: Noticeably worse without it, but functional.
Nice-to-have: Would be great, but nobody would notice its absence.

### Step 2: Cut from the bottom
Remove all nice-to-haves first. Then should-haves if still over budget.
Never cut must-haves — instead, reduce their scope.

### Step 3: Reduce, don't remove
If [a must-have feature is too expensive] → implement the simplest version that works.
A booking calendar with 3 features is better than no booking calendar.
A payment flow with mock payment is better than no payment flow.

## Traps to Avoid
- Cutting quality instead of features: Never skip QA, responsive, accessibility. Cut features.
- "We'll add it later": Later never comes. Either it's in scope or it's explicitly not.
