# Routine: Code Complete Check

## When to Run
Before marking any code unit (function, component, module) as done.

## Checklist
- [ ] All acceptance criteria met
- [ ] Error states handled (network failure, invalid input, empty data)
- [ ] Loading states shown during async operations
- [ ] Empty states shown when no data exists
- [ ] No TODO comments remain
- [ ] No console.log statements remain
- [ ] No commented-out code remains
- [ ] Types are complete (no `any`)
- [ ] File follows naming convention (kebab-case)

## If Any Check Fails
Fix it. This takes 2 minutes. Skipping it costs 20 minutes later.

## Duration
2 minutes per code unit.
