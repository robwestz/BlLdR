# Constraint: No Inline Styles

## Scope
Always. All JSX/HTML files.

## Prohibited Patterns

### ❌ Style attribute
**Banned:** `style={{ color: 'red', margin: '10px' }}` or `style="color: red"`
**Why:** Inline styles override all CSS specificity, making theme changes impossible. They also scatter styling logic across every component.
**Instead:** Use Tailwind utilities (`className="text-red-500 m-2"`) or CSS classes

### ❌ Dynamic inline styles for theming
**Banned:** `style={{ backgroundColor: theme.primary }}` in components
**Why:** Breaks when theme changes; not cacheable; not responsive-aware.
**Instead:** Set CSS custom properties on :root, reference them in classes
