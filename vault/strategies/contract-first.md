# Strategy: Contract-First Development

## When to Apply
When building modules that will interface with each other, or with external systems.

## The Approach

### Step 1: Define the interface before the implementation
What data goes in? What data comes out? What errors are possible?
Write this as a TypeScript type or a contract.md file.

### Step 2: Lock the contract
Once defined, the contract does not change without explicit versioning.
Both sides (producer and consumer) must agree.

### Step 3: Implement against the contract
The implementation is free to do anything internally, as long as the external contract holds.
If [implementation can't meet the contract] → update the contract, bump the version, notify dependents.

## Traps to Avoid
- Implementing first, defining contract after: The contract shapes the implementation, not vice versa.
- Changing the contract silently: Always bump version. Always notify.
