# Routine: Post-Module QA

## When to Run
After completing every module, before starting the next.

## Checklist
- [ ] Module builds without errors
- [ ] All acceptance criteria from the module spec are met
- [ ] No console errors in the browser
- [ ] Responsive layout works at 320px, 768px, 1024px
- [ ] No placeholder text visible ("Lorem ipsum", "TODO", "example@")
- [ ] No hardcoded colors (all via CSS variables)
- [ ] No inline styles
- [ ] All interactive elements have hover/focus states
- [ ] state/orchestration.yaml updated with loc_consumed

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not proceed to the next module.

## Duration
3-5 minutes per module.
