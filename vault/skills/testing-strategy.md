# Skill: Testing Strategy

## When to Use
Planning or writing tests for any module.

## Steps
1. Identify the critical path: what user flow MUST work
2. Write one end-to-end test for the critical path first
3. For each component: test the contract (props in → rendered output)
4. For each utility function: test edge cases (empty input, null, boundary values)
5. For API endpoints: test success (200), validation error (400), not found (404)
6. Skip testing: pure UI layout, third-party library wrappers, config files
7. Name tests as sentences: "should show error when email is invalid"

## Verification
- [ ] Critical path has at least one end-to-end test
- [ ] Each component tests its prop interface
- [ ] Edge cases covered for utility functions
- [ ] Tests run without manual setup

## Common Mistakes
- Testing implementation details: Test behavior, not internal state
- 100% coverage goal: Cover critical paths, not getters and setters
- Tests that need manual steps: Tests must run with one command
