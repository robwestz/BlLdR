# Routine: Pre-Deployment Verification

## When to Run
Before any production deployment, regardless of project type.

## Checklist
- [ ] Full build/compile succeeds with zero errors (`npm run build`, `python -m build`, `go build`, etc.)
- [ ] All automated tests pass with zero failures
- [ ] Linter passes with zero errors
- [ ] No secrets, API keys, or tokens present in the artifact being deployed
- [ ] Environment variables required in production are documented and confirmed present
- [ ] Every critical user flow verified manually or by smoke test (not just "it compiles")
- [ ] Rollback plan exists: if this deploy fails, what is the exact procedure to revert?
- [ ] Monitoring/alerting is active and will surface errors within 5 minutes of deploy

## If Any Check Fails
Fix the issue. Re-run the full checklist. Do not deploy until all pass.

## Duration
10 minutes.

---
*Web frontends: also run `performance-check.md` and `accessibility-audit.md` post-deploy.*
*APIs: also run `security-check.md` before exposing to traffic.*
