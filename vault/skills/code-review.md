# Skill: Code Review

## When to Use
After completing any module or unit of code, before marking it done
and before passing it to the next module.

## Steps
1. Read the code top-to-bottom once without commenting — form a structural view
2. Check correctness: does every function do what its name says?
3. Check error handling: what happens when any input is null, empty, or wrong type?
4. Check state: is every side effect intentional and contained?
5. Check dependencies: is every import used? Is every import necessary?
6. Check duplication: is any logic repeated that could be a shared function?
7. Check naming: does every variable/function name describe what it contains/does?
8. Check boundaries: does the module do ONLY what it's supposed to do?
9. List findings by severity: blocking (must fix), important (should fix), minor (nice to fix)
10. Fix all blocking findings before declaring review complete

## Verification
- [ ] No function does more than one thing (fails if AND appears in the name)
- [ ] Every error path returns a typed error response, not undefined/null silently
- [ ] No TODO or FIXME comments remain in committed code
- [ ] All external inputs are validated before use
- [ ] No unused variables or imports
- [ ] The module's public interface matches the contract it was supposed to implement

## Common Mistakes
- Reviewing while writing: Review is a separate pass — context switching degrades both
- Flagging style over substance: Only flag style if a linter can't catch it automatically
- Missing error paths: "Happy path works" is not complete review — check every rejection
- Skipping the boundary check: Modules that do too much are the #1 source of later bugs
