# Skill: Remote Data Fetching

## When to Use
Fetching, caching, and displaying any data from an external source (API, database,
or server function) in a UI component.

## Steps
1. Define the three display states before writing fetch logic: loading / error / success
2. Set loading state to true BEFORE the request begins
3. Wrap the request in try/catch — never assume success
4. On error: store the error message, not the error object
5. On success: validate that the response shape matches the expected type
6. Set loading state to false in BOTH success and error paths (use finally)
7. Cache results if the same data is fetched in multiple places:
   - Same page → local state lifted to parent
   - Cross-page → query cache (React Query, SWR, or equivalent)
   - Rarely changes → HTTP cache headers at the API level
8. Add a re-fetch trigger if data can go stale (user action, interval, or focus event)
9. Abort in-flight requests when the component unmounts (AbortController)

## Verification
- [ ] Loading spinner or skeleton appears before data arrives
- [ ] Error message is user-readable and specific (not "An error occurred")
- [ ] Empty response (empty array, null data) has distinct empty state — not a generic error
- [ ] Request cannot be triggered twice simultaneously (button disabled during fetch)
- [ ] No memory leaks: component cleanup cancels pending requests

## Common Mistakes
- Showing nothing while loading: Users assume the page broke — always show a loading state
- Catching errors but not setting error state: Error is swallowed, nothing updates in the UI
- Not handling empty vs null: null means "failed", [] means "none exist" — design both
- Re-fetching on every render: useEffect with missing dependency array causes infinite loops
