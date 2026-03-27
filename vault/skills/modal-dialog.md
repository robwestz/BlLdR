# Skill: Modal Dialog

## When to Use
Presenting focused content or a required decision that must be resolved before the user continues.

## Steps
1. Store a reference to the element that triggered the modal open
2. When opening: add `overflow: hidden` to `<body>` to prevent background scroll
3. Move DOM focus to the first focusable element inside the modal immediately on open
4. Implement focus trap: Tab cycles forward through modal focusables, Shift+Tab cycles backward — focus never leaves
5. Close the modal on Escape key press
6. Add a visible close button (×) that closes the modal
7. Optionally close on backdrop click — make this configurable, not always-on
8. Add `role="dialog"`, `aria-modal="true"`, and `aria-labelledby` pointing to the modal's heading
9. On close: remove `overflow: hidden` from body and return focus to the stored trigger element
10. Never nest one modal inside another — chain them sequentially instead

## Verification
- [ ] Tab key cycles only through elements inside the open modal
- [ ] Escape key closes the modal
- [ ] Focus returns to the trigger element after close
- [ ] Body scroll is locked while modal is open and restored after close
- [ ] Modal has role="dialog" and aria-labelledby set to its heading id
- [ ] Screen reader announces the modal heading when it opens

## Common Mistakes
- Not trapping focus: Tab escapes to background content → implement a focus trap loop
- Losing trigger reference: Focus goes to `<body>` on close, disorienting keyboard users → store trigger before open
- Nesting modals: Creates inaccessible, confusing UX → close the first before opening a second
- Hardcoding backdrop-click-to-close: Sometimes users accidentally dismiss → make it opt-in per instance
