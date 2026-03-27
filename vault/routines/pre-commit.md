# Routine: Pre-Commit

## When to Run
Before every git commit, without exception.

## Checklist
- [ ] No debug statements in staged files (console.log, print, debugger, var_dump)
- [ ] No .env or secrets file appears in `git diff --cached`
- [ ] No TODO or FIXME in newly added lines (pre-existing ones are exempt)
- [ ] No commented-out code blocks of 3 or more consecutive lines
- [ ] No unintended binary or temp files in staged list (`git diff --cached --name-only`)
- [ ] Test suite passes with zero failures (`npm test`, `pytest`, or equivalent)
- [ ] Linter passes with zero errors (`eslint`, `ruff`, `rubocop`, or equivalent)

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not commit until all checks pass.

## Duration
3-5 minutes.
