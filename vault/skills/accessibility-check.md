# Skill: Accessibility Verification

## When to Use
After building any visual component or page.

## Steps
1. Check color contrast: text vs background ≥ 4.5:1 (WCAG AA)
2. Check large text contrast: ≥ 3:1 for text 18px+ or 14px+ bold
3. Verify all images have meaningful alt text (not "image" or "photo")
4. Verify all form inputs have associated labels (not just placeholder)
5. Tab through the page: every interactive element must be reachable
6. Verify focus indicators are visible on all focusable elements
7. Verify buttons have accessible names (text content or aria-label)
8. Check heading hierarchy: h1 → h2 → h3, no skipped levels

## Verification
- [ ] Text contrast ≥ 4.5:1
- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Tab navigation reaches every interactive element
- [ ] Focus indicators visible
- [ ] Heading hierarchy is sequential

## Common Mistakes
- Placeholder as label: Placeholder disappears on focus; use <label>
- "Click here" link text: Link text must describe the destination
- Decorative images with alt text: Use alt="" for purely decorative images
