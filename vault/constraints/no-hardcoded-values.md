# Constraint: No Hardcoded Values

## Scope
Always. All file types.

## Prohibited Patterns

### ❌ Magic numbers
**Banned:** Numeric literals in logic or styles (e.g., `margin: 24px`, `if (count > 5)`)
**Why:** Changing the value requires finding every occurrence; missed ones cause bugs.
**Instead:** Define as named constant or CSS variable: `--spacing-lg: 1.5rem`, `const MAX_RETRIES = 5`

### ❌ Hardcoded colors
**Banned:** Color values directly in components (`color: #2563EB`, `bg-blue-600`)
**Why:** Theme changes require find-and-replace across all files; missed ones break visual consistency.
**Instead:** Use CSS custom properties: `color: var(--color-primary)`

### ❌ Hardcoded strings
**Banned:** User-visible text directly in components (`<h1>Welcome</h1>`)
**Why:** Translation, copy changes, and A/B testing all require code changes.
**Instead:** Use constants file or i18n keys: `<h1>{t('welcome.heading')}</h1>`

### ❌ Hardcoded URLs
**Banned:** API endpoints or external URLs as string literals in components
**Why:** Environment changes (dev→staging→prod) require code changes.
**Instead:** Use environment variables or config: `const API = config.apiUrl`
