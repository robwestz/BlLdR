# Constraint: No Console Output in Production

## Scope
Always. All JavaScript/TypeScript files.

## Prohibited Patterns

### ❌ console.log
**Banned:** `console.log()` in any committed code
**Why:** Client opens DevTools and sees debug messages. Looks unprofessional. Leaks internal data.
**Instead:** Remove entirely, or use a logger utility that is disabled in production.

### ❌ console.warn / console.error for debugging
**Banned:** Using console.warn/error as debugging aids left in code
**Why:** Clutters the console; real warnings/errors become invisible in the noise.
**Instead:** Fix the issue or remove the log. Legitimate error logging uses a structured logger.
