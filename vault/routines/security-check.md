# Routine: Security Check

## When to Run
Before exposing any endpoint or service to the internet.

## Checklist
- [ ] No API keys, tokens, or passwords in source code (grep: `sk-`, `Bearer `, `password =`, `secret =`)
- [ ] All user inputs validated server-side, not only client-side
- [ ] All database queries use parameterized statements — no string concatenation with user input
- [ ] Every non-public endpoint requires authentication
- [ ] Error responses return generic messages — no stack traces or internal paths
- [ ] File upload endpoints validate MIME type and file size server-side
- [ ] CORS is restricted to specific origins — wildcard `*` is not present in production config
- [ ] Rate limiting is active on authentication and sensitive endpoints

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not expose the endpoint until all checks pass.

## Duration
5-10 minutes.
