# Skill: Contract Authoring

## When to Apply
Creating or updating interface contracts between modules (contracts/[module-id].md).

## Steps

1. Open the contract file for this module.
2. Under "Interfaces", define:
   - **Data entities**: exact field names, types, constraints (from module data model).
   - **API endpoints**: method, path, request body shape, response shape, error codes.
   - **Component props**: name, type, required/optional, description.
3. Under "Decisions", record every architecture choice with rationale.
4. Under "Non-goals", list what this module does NOT handle.
5. Bump CONTRACT_VERSION when changing any interface.
6. Notify dependent modules (check depends_on in other module specs).

## Common Mistakes
- Writing vague interfaces ("handles data") instead of concrete shapes.
- Forgetting error response shapes — consumers need to handle failures.
- Not bumping CONTRACT_VERSION — downstream modules use stale contracts.
- Defining component props without types — leads to runtime prop mismatches.

## Verification
- Every data field has a type (not just a name).
- Every API endpoint has request AND response shapes.
- Every component has typed props.
- CONTRACT_VERSION is incremented from previous value.
