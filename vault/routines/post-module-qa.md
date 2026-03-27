# Routine: Post-Module QA

## When to Run
After completing every module, before starting the next.
Applies to all module types: UI, API, CLI, data, service.

## Checklist
- [ ] Module builds/compiles without errors
- [ ] All acceptance criteria from the module spec are met
- [ ] No placeholder values visible (test data, example text, hardcoded IDs)
- [ ] All error paths return a response — no silent failures or unhandled exceptions
- [ ] No TODO comments remain in code added this module
- [ ] No debug statements in committed code (console.log, print, debugger)
- [ ] `state/orchestration.yaml` updated: module marked complete, `loc_consumed` recorded

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not proceed to the next module.

## Duration
3-5 minutes per module.

---
*UI modules: also run `responsive-verify.md` and `accessibility-audit.md`.*
