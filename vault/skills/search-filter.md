# Skill: Search and Filter

## When to Use
Any interface where users need to find or narrow down items from a list.

## Steps
1. Debounce search input by 300ms before triggering a query or filter pass
2. Decide execution location: ≤500 items → filter client-side in memory; >500 items → send query to server
3. Persist all active filters and the search term in the URL query string
4. Apply filters and search together in a single pass — never chain sequential re-renders
5. Display active filter count on any collapsed filter panel ("Filters (3)")
6. Show a "Clear all filters" button whenever at least one filter is active
7. Show an empty state message when results are zero — include a reset action in the message
8. For server-side search, cancel the in-flight request before sending the next one (abort signal)

## Verification
- [ ] Sharing the URL reproduces the exact same filtered view
- [ ] Typing quickly fires only one request after the user stops (debounce working)
- [ ] "Clear all" resets every filter and the search term in one action
- [ ] Zero-results state includes a visible way to reset
- [ ] Active filter count badge updates immediately when a filter is toggled
- [ ] Stale results from a previous request do not appear after a faster subsequent request

## Common Mistakes
- Filtering on every keystroke: Causes thrashing on server and jank on client → debounce 300ms
- Storing filter state only in component memory: Refresh loses context → sync to URL
- Separate "Apply" button for filters: Adds friction for obvious non-destructive actions → filter on change
- No empty state: Users assume the product is broken → always show a message with a reset path
- Race conditions on async search: Slow responses overwrite fast ones → cancel previous requests
