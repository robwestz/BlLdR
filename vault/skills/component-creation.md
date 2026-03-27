# Skill: Component Creation

## When to Use
Creating any reusable UI component.

## Steps
1. Define TypeScript interface for all props (name, types, optionality)
2. Set sensible defaults for optional props
3. Create the component as a function component
4. Implement visual variants (primary/secondary/ghost) via a `variant` prop
5. Add hover, focus, active, and disabled states
6. Use CSS variables or Tailwind utilities — never inline styles
7. Ensure keyboard accessibility (focusable, enter/space triggers action)
8. Add aria attributes where needed (aria-label, role, aria-disabled)
9. Export the component and its prop types

## Verification
- [ ] Props interface is exported and complete
- [ ] All variants render correctly
- [ ] Hover/focus/active states are visually distinct
- [ ] Disabled state is visually muted AND non-interactive
- [ ] Component works with keyboard only (no mouse)
- [ ] No inline styles used

## Common Mistakes
- Missing disabled state: Always handle disabled visually AND functionally
- Props without types: Every prop must have a TypeScript type
- Hardcoded colors: Use CSS variables or design tokens
- Missing focus indicator: Users who tab must see where focus is
