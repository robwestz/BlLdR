# Strategy: Tech Choice

## When to Apply
When choosing between technology options: libraries, databases, protocols, frameworks, tools.

## The Approach

### Step 1: List What You Actually Need
Write down the concrete requirements — not features that sound useful, only what the current problem demands.
Ask: What does this need to do today? What will it definitely need in 3 months?

### Step 2: Check the Built-In Option First
Does the standard library or existing stack already cover 80% of the need?
Check what you already have before adding a dependency.

### Step 3: Evaluate Fit and Health
- Maintenance: When was the last commit? Are issues being closed?
- Stack fit: Same language ecosystem? Integrates with existing auth, logging, config?
- Production usage: Is there evidence this is used at similar scale to yours?

### Step 4: Prototype the Riskiest Part
Spend 30 minutes testing the one thing most likely to fail.
Do not commit to a choice before the prototype runs.

## Decision Points
If built-in covers 80% of the need → use it, don't add a dependency.
If one option has significantly more production usage in your domain → default to it.
If options are genuinely equivalent → pick the one your team already knows.
If the 30-minute prototype fails → eliminate that option before evaluating further.

## Traps to Avoid
- Choosing by popularity contest: Stars don't mean fit. Evaluate against your actual requirements.
- Choosing what worked at a previous job: Context differs. Evaluate fresh.
- Avoiding learning as a criterion: "We don't know it" is a cost, not a disqualifier.
