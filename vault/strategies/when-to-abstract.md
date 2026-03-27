# Strategy: When to Abstract

## When to Apply
Deciding whether to create a generic abstraction or keep code concrete.

## The Approach

### Step 1: Count the instances
How many times does this pattern appear (or will it appear)?

### Step 2: Decide
If [1 instance] → keep it concrete. No abstraction.
If [2 instances] → tolerate the duplication. Note it for later.
If [3+ instances] → extract the abstraction now.
If [the pattern is in a shared contract] → abstract regardless of count.

### Step 3: Verify the abstraction
Does the abstraction make the code shorter? If not, it's not helping.
Can someone understand the abstraction without reading its implementation? If not, it's too clever.

## Traps to Avoid
- Premature abstraction: Abstracting on the first occurrence wastes tokens and adds complexity.
- "Just in case" abstractions: Build what you need, not what you might need.
