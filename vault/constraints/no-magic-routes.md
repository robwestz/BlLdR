# Constraint: No Magic Routes

## Scope
Always. All files containing navigation, links, redirects, or URL construction.

## Prohibited Patterns

### ❌ Inline string literals for routes
**Banned:** `href="/dashboard/settings"` or `router.push('/account/billing')` as raw strings
**Why:** Renaming a route requires grepping the entire codebase; missed occurrences break silently at runtime.
**Instead:** Use a route constants file: `href={ROUTES.dashboard.settings}` or `router.push(ROUTES.account.billing)`.

### ❌ String concatenation to build URLs
**Banned:** `"/users/" + userId` or `` `/orders/${orderId}/details` `` constructed inline
**Why:** URL shape is duplicated across callers; a structural change (e.g. adding a prefix) breaks all variants except the one the developer remembered.
**Instead:** Define a typed factory in the constants file: `ROUTES.users.detail(userId)` that owns the shape in one place.

### ❌ Redirect targets as bare strings in server code
**Banned:** `redirect('/login')` or `res.redirect('/auth/signin')` without a constant
**Why:** Auth redirect paths drift between server and client code; a mismatch causes infinite redirect loops in production.
**Instead:** `redirect(ROUTES.auth.login)` — both server and client code reference the same constant.
