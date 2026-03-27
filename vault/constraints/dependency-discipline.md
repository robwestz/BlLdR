# Constraint: Dependency Discipline

## Scope
Always. Package.json / requirements.txt additions.

## Prohibited Patterns

### ❌ Unjustified dependencies
**Banned:** Adding an npm package without explicit justification
**Why:** Each dependency adds bundle size, security surface, and maintenance burden.
**Instead:** Before adding: (1) Can stdlib do this? (2) Is the package actively maintained? (3) Does it save >50 lines of code?

### ❌ Utility libraries for single functions
**Banned:** Adding lodash for one function, moment.js for date formatting
**Why:** Massive bundle impact for trivial utility.
**Instead:** Write the 5-line utility function. Use native Date API. Use Array methods.

### ❌ Multiple libraries for the same purpose
**Banned:** Both axios and fetch wrappers, both dayjs and date-fns
**Why:** Confusion, inconsistency, bloat.
**Instead:** Choose one. Document the choice. Use it consistently.
