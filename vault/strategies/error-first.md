# Strategy: Error-First Development

## When to Apply
Implementing any feature that can fail (API calls, forms, data loading).

## The Approach

### Step 1: List failure modes
Before writing the happy path, list everything that can go wrong.
Network down. Invalid input. Empty response. Auth expired. Rate limited.

### Step 2: Build error UI first
Design and implement the error states before the success state.
If [network error] → show retry button + offline message
If [validation error] → show inline field errors
If [empty data] → show empty state with action suggestion
If [auth error] → redirect to login with message

### Step 3: Then build the happy path
With error handling already in place, the happy path is straightforward.

## Traps to Avoid
- "I'll add error handling later": Later means it won't happen. Handle errors first.
- Catch-all error message: "Something went wrong" is lazy. Tell the user WHAT and WHAT TO DO.
