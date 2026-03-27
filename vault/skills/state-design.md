# Skill: State Design

## When to Use
Deciding where any piece of mutable data should live in a UI application.

## Steps
1. Identify every piece of mutable data: what changes during the session?
2. Classify each piece by scope and lifetime:
   - **Local UI state** (open/closed, selected tab): lives in the component that owns it
   - **Form state** (input values, validation errors): lives in the form component or a form library
   - **Server state** (fetched data): fetched on demand, cached at the data layer — not duplicated in component state
   - **URL state** (current page, active filters, selected ID): lives in the URL query string — makes the view shareable and bookmarkable
   - **Shared state** (used by 2+ unrelated components): lift to the nearest common ancestor, or use a dedicated store/context
   - **Persistent state** (survives page reload): stored via a storage adapter (localStorage, sessionStorage, server API) — never raw direct storage calls in components
3. Default: keep state as local as possible. Lift only when two independent components genuinely need the same value.
4. If unsure: ask "does another component NEED to read or write this?" If no → keep it local.

## Verification
- [ ] No global store contains data that is only used in one component
- [ ] URL query string reflects all state a user would want to share or bookmark
- [ ] Server data is not duplicated into local component state on fetch
- [ ] Persistent values go through a storage adapter, not direct localStorage in the render tree

## Common Mistakes
- Everything in global state: state shared globally causes invisible coupling — keep state local until proven otherwise
- Duplicating fetched data locally: leads to stale state divergence — let the data layer own server data
- Transient UI state in the URL: modal open/closed, tooltip visible — URL should reflect navigation intent, not component state
- Not using URL for filter/pagination state: users lose position on refresh and can't share their view
