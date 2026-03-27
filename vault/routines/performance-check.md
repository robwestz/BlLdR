# Routine: Performance Check

## When to Run
After every deployment to a production or staging environment.

## Checklist
- [ ] Main page load is under 3 seconds on simulated 3G (Lighthouse or equivalent)
- [ ] Largest Contentful Paint (LCP) is under 2.5 seconds (Lighthouse report)
- [ ] Every image has explicit width and height attributes set
- [ ] Initial JavaScript payload is under 200KB gzipped (or within the agreed project budget)
- [ ] No N+1 query pattern detected in database logs for the main user flows
- [ ] All API endpoints respond in under 500ms under normal load

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not mark the deployment as stable until all checks pass.

## Duration
10-15 minutes.
