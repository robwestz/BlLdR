# Strategy: Preflight Reopen

## When to Apply
Deciding whether approved preflight architecture may be changed after approval.

## The Approach

### Step 1: Classify the change
What is being changed? Purpose (CRI), architecture (minimal set), acceptance criteria, or a recorded decision?

### Step 2: Decide
If [change affects CRI fields — target users, monetization, business outcome] → reopen required. New run from Phase 1.
If [change adds or removes a component from the minimal-inevitable set] → reopen required. New run from Phase 3.
If [change contradicts a recorded decision in PREFLIGHT_DECISIONS.json] → conflict protocol. User chooses reopen or explicit deviation.
If [change is within approved scope — implementation detail, wave order, vault selection, design choices] → no reopen needed.
If [new information materially changes purpose or constraints] → reopen required. User must confirm.

### Step 3: Execute
Reopen = new preflight run from the affected phase. All downstream phases rerun.
Previous approved artifacts are preserved (new timestamped slug if collision).
Never modify existing approved artifacts — always create new ones.

## Traps to Avoid
- Using "accept deviation" as a backdoor to avoid reopen. Each deviation needs a recorded decision with `owner_of_decision: user_explicit`.
- Reopening for implementation details. Tech stack choice within an approved component is not a reopen trigger — it is operator's domain.
