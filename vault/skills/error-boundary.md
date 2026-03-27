# Skill: Error Boundary

## When to Use
Wrapping React UI sections to catch render errors and show fallback UI instead of a white screen.

## Steps
1. Create an `ErrorBoundary` class component implementing `getDerivedStateFromError` and `componentDidCatch`
2. Accept a `fallback` prop for custom fallback UI — never expose technical error messages to end users
3. Wrap each major page section in its own boundary (not the entire app in a single boundary)
4. Log the caught error inside `componentDidCatch` to your error tracking service (e.g. Sentry)
5. Add a "Try again" button in the fallback UI that calls `this.setState({ hasError: false })`
6. In production: show a friendly message only; in development: render the error stack for debugging

## Verification
- [ ] Throwing inside a child component shows fallback UI, not a blank screen
- [ ] The caught error is sent to the error tracking service on every occurrence
- [ ] "Try again" button resets the boundary and re-renders the child tree
- [ ] No error stack trace or raw `error.message` is visible to users in production builds

## Common Mistakes
- One boundary around the whole app: a single crash blacks out the entire UI → wrap each major section independently
- Swallowing errors without logging: the bug becomes invisible in production → always log in `componentDidCatch`
- Showing `error.message` to users: leaks implementation details and confuses users → show a static friendly message
- Resetting state on every re-render: causes infinite retry loops → reset only on explicit user action
