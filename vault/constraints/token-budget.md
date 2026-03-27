# Constraint: Token Budget Discipline

## Scope
Always. Agent-generated code.

## Prohibited Patterns

### ❌ Excessive comments
**Banned:** Comments exceeding 15% of total code lines in a file
**Why:** Comments cost tokens equal to code but produce zero functionality. Every comment line is a code line you didn't write.
**Instead:** Use TypeScript types for documentation. Well-named functions are self-documenting. Comment only genuinely non-obvious logic.

### ❌ Boilerplate expansion
**Banned:** Generating verbose patterns when concise alternatives exist
**Why:** Token budget is finite. Verbose code reduces the number of features deliverable.
**Instead:** Use config-driven patterns, generic hooks, type-driven rendering.

### ❌ Speculative code
**Banned:** Writing code "we might need later" that isn't in the current wave
**Why:** Consumes budget now for uncertain future value. YAGNI.
**Instead:** Build what the current wave specifies. Future waves plan themselves.
