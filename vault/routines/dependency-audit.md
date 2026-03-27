# Routine: Dependency Audit

## When to Run
When adding or updating any package or library dependency.

## Checklist
- [ ] Every new dependency has a documented justification (one sentence minimum)
- [ ] New dependency's last published release is within the past 6 months
- [ ] New dependency's license is compatible with the project (MIT/Apache/BSD pass; GPL requires explicit sign-off)
- [ ] No existing dependency already covers the same functionality
- [ ] `npm audit` (or `pip-audit`, `bundle audit`, or equivalent) reports zero high or critical vulnerabilities
- [ ] Build size measured before and after — increase is within the agreed bundle budget

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not merge the dependency until all checks pass.

## Duration
5 minutes per new dependency.
