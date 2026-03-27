# Constraint: Code Hygiene

## Scope
Always. All source files.

## Prohibited Patterns

### ❌ Commented-out code
**Banned:** Blocks of code commented out "for later" or "just in case"
**Why:** Creates confusion about what is active. Version control is the backup.
**Instead:** Delete it. Git has the history if you need it back.

### ❌ Unused imports
**Banned:** Import statements for symbols not used in the file
**Why:** Confuses readers, may prevent tree-shaking, triggers linter warnings.
**Instead:** Remove unused imports before committing.

### ❌ Unused variables
**Banned:** Variables declared but never read
**Why:** Indicates incomplete refactoring or dead logic paths.
**Instead:** Remove, or prefix with underscore if required by destructuring.

### ❌ Duplicated logic
**Banned:** Same logic written in two or more places
**Why:** Bug fix in one location misses the other. Guaranteed drift.
**Instead:** Extract to a shared function. Import from one location.
