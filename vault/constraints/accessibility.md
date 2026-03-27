# Constraint: Accessibility Requirements

## Scope
Always. All visual UI components.

### ❌ Images without alt text
**Banned:** `<img>` without alt attribute
**Why:** Screen readers announce nothing. Decorative images need `alt=""` explicitly.
**Instead:** Meaningful alt text for content images, `alt=""` for decorative.

### ❌ Form inputs without labels
**Banned:** `<input>` without associated `<label>`
**Why:** Screen readers can't identify the field. Placeholder is not a label.
**Instead:** `<label htmlFor="id">` paired with `<input id="id">`.

### ❌ Low contrast text
**Banned:** Text with contrast ratio below 4.5:1 against its background
**Why:** Unreadable for users with low vision. Fails WCAG AA.
**Instead:** Check contrast ratio. Use darker text or lighter background.

### ❌ Non-keyboard-accessible interactions
**Banned:** Click-only interactions with no keyboard equivalent
**Why:** Users who can't use a mouse are locked out.
**Instead:** All interactive elements focusable and operable with Enter/Space.
