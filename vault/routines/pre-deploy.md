# Routine: Pre-Deployment Verification

## When to Run
Before any production deployment.

## Checklist
- [ ] `npm run build` completes without errors
- [ ] `npm run preview` serves the site correctly
- [ ] Every page/route loads without errors
- [ ] Browser console shows zero errors and zero warnings
- [ ] All images and assets load (no 404s in network tab)
- [ ] Meta tags present on all pages (title, description, OG)
- [ ] Favicon displays correctly
- [ ] Mobile layout verified at 320px
- [ ] Lighthouse performance ≥ 90

## If Any Check Fails
Fix the issue. Re-run the full checklist. Do not deploy until all pass.

## Duration
10 minutes.
