# Skill: State Management Design

## When to Use
Deciding where application state should live.

## Steps
1. Identify the state: what data changes during the session?
2. Classify each piece: UI state, server state, URL state, or form state
3. UI state (open/closed, selected tab) → useState in the component
4. Form state (input values, validation) → useFormState or useState
5. Server state (fetched data) → fetch + useState, or a data-fetching hook
6. URL state (current page, filters) → router/URL params
7. Shared state (used by 2+ unrelated components) → Context or lift state up
8. Persistent state (survives page reload) → storage adapter (localStorage/API)
9. Default rule: keep state as LOCAL as possible. Lift only when proven needed.

## Verification
- [ ] No global state for component-local concerns
- [ ] URL reflects filterable/shareable state
- [ ] Server data is fetched, not duplicated in local state
- [ ] Persistent state uses the storage adapter, not direct localStorage

## Common Mistakes
- Everything in global state: Keep state local until lifting is necessary
- Duplicating server data in local state: Fetch, don't copy
- Not using URL for shareable state: Filters, pagination belong in the URL
