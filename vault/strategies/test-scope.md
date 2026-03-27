# Strategy: Test Scope

## When to Apply
When deciding what to test, how much to test, and when to skip writing a test.

## The Approach

### Step 1: Classify the Code
Is this logic or plumbing?
- Logic: business rules, calculations, data transformations, permission checks.
- Plumbing: framework wiring, config loading, trivial getters, generated boilerplate.
Logic deserves tests. Plumbing rarely does.

### Step 2: Ask the Silent Failure Question
If this breaks, would you notice immediately during normal use?
If yes → lower test priority. If no → test it; silent failures are the dangerous kind.

### Step 3: Assess Branching Complexity
Does this function have multiple paths, edge cases, or inputs that change behavior?
If yes → test the branches, not just the happy path.

## Decision Points
Always test: pure functions with business logic, financial calculations, auth and permission checks, data transformations with edge cases.
Skip testing: framework-generated boilerplate, one-line wrappers, anything that fails loudly at compile or boot time.
If unsure → ask: would a future developer be confused about what this is supposed to do? If yes, a test documents intent.

## Traps to Avoid
- Testing implementation instead of behavior: Tests that break on refactor protected nothing — they only tracked how the code was written.
- Writing tests after the code with no new insight: A test written only to hit coverage adds maintenance cost without protection.
- "We'll add tests later": Later does not come. Untested logic accumulates until the cost of testing exceeds the cost of rewriting.
