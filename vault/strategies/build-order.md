# Strategy: Build Order

## When to Apply
Deciding which module or feature to build next.

## The Approach

### Step 1: Map dependencies
List what each module needs to exist before it can be built.

### Step 2: Identify the critical path
If A depends on B depends on C → build C first.
If A and B are independent → build whichever reduces risk more.

### Step 3: Decide
If [module has zero dependencies] → it can be built in any order.
If [module is depended on by 3+ others] → build it early (it's load-bearing).
If [two modules are equal priority] → build the one that produces visible output first (motivates the team/client).
If [unsure] → build foundation → design system → core feature → enhancements → deploy. This order always works.

## Traps to Avoid
- Building "the fun part" first: Fun modules often depend on boring ones. Build the boring ones.
- Parallelizing modules that share state: Finish one, then start the other.
