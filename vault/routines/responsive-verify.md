# Routine: Responsive Verification

## When to Run
After any visual change to any component or page.

## Checklist
- [ ] 320px: no horizontal scroll, text readable, buttons tappable (≥44px)
- [ ] 768px: layout adapts appropriately (2-column, sidebar, expanded cards)
- [ ] 1024px: full desktop layout renders correctly
- [ ] No overlapping elements at any breakpoint
- [ ] Images scale without distortion at all breakpoints
- [ ] Navigation is accessible at all breakpoints (hamburger on mobile)

## If Any Check Fails
Fix the CSS at the failing breakpoint. Do not override with !important. Re-run checklist.

## Duration
2 minutes.
