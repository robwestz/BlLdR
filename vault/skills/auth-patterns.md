# Skill: Authentication Patterns

## When to Use
Building any system with user accounts.

## Steps
1. Choose auth strategy: session-based (traditional) or token-based (JWT/API)
2. Build registration form: email + password + confirm password
3. Hash passwords server-side (never store plaintext, never hash client-side)
4. Build login form: email + password → receive token/session
5. Store auth token securely (httpOnly cookie preferred, localStorage acceptable)
6. Create auth context/provider that exposes: user, login(), logout(), isAuthenticated
7. Build protected route wrapper: redirects to login if not authenticated
8. Build logout: clear token/session, redirect to public page
9. Handle token expiry gracefully: redirect to login with "session expired" message

## Verification
- [ ] Registration creates account and logs in
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials shows error (not "user not found" — just "invalid credentials")
- [ ] Protected routes redirect to login when unauthenticated
- [ ] Logout clears session and redirects
- [ ] Page refresh preserves logged-in state

## Common Mistakes
- "User not found" vs "wrong password": Always generic "invalid credentials" (prevents user enumeration)
- Storing password in state: Password leaves the form, goes to API, never stored client-side
- Protected pages before auth works: Auth must be complete before building protected features
