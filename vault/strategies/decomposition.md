# Strategy: Task Decomposition

## When to Apply
Any task that feels large, vague, or multi-step.

## The Approach

### Step 1: Name the output
What specific artifact does this task produce? A file? A component? A deployed page?

### Step 2: List dependencies
What must exist before this task can start?

### Step 3: Break into steps where each produces a verifiable result
Bad: "Build the booking system"
Good: "1. Create BookingForm component (renders 3 fields) 2. Add date picker 3. Connect to API 4. Show confirmation"

### Step 4: Estimate each step independently
If [any step > 100 lines] → decompose that step further
If [any step has unclear output] → define the output first

## Traps to Avoid
- Steps without outputs: Every step must produce something testable
- Decomposing too fine: 3-10 steps per task. Not 30.
