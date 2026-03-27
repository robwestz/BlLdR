# Routine: API Endpoint Check

## When to Run
After implementing any new API endpoint, before marking it complete.

## Checklist
- [ ] Endpoint returns the correct HTTP status code for every case: 200/201, 400, 401/403, 404, 500
- [ ] Error responses follow the project's standard error format (`{ error, code }` or equivalent) — no raw exceptions
- [ ] Input is validated server-side before any business logic runs
- [ ] Authentication is enforced — unauthenticated request returns 401, not 200 with empty data
- [ ] Response body shape matches the declared contract in `contracts/`
- [ ] Endpoint does not expose internal paths, stack traces, or database IDs that should be hidden
- [ ] At least one unhappy-path case manually tested: missing required field, invalid format, unauthorized

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not mark the endpoint as complete.

## Duration
5 minutes per endpoint.
