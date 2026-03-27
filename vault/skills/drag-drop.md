# Skill: Drag and Drop

## When to Use
Letting users reorder items in a list or move items between defined zones via direct manipulation.

## Steps
1. Set `draggable="true"` on each item and attach `dragstart`, `dragover`, `dragend` event handlers
2. On `dragstart`: record the dragged item's index; set opacity to 0.5 on the dragged element
3. On `dragover` of a drop target: add a visible highlight class and call `event.preventDefault()`
4. On `drop`: swap or insert the item at the new index; remove all highlight classes
5. On `dragend`: reset opacity to 1 regardless of whether the drop succeeded
6. Implement touch support: listen to `touchstart`, `touchmove`, `touchend` with the same index-swap logic
7. Provide a keyboard alternative: when an item has focus, Up/Down arrows move it one position; Enter or Space commits
8. Announce the new position to screen readers after a successful move (`aria-live="polite"`)
9. Persist the new order to the backend immediately after drop — do not wait for a separate save action
10. Show a placeholder element in the drop target position during drag to communicate where the item will land

## Verification
- [ ] Dragged item shows reduced opacity during drag
- [ ] Drop target zone highlights when a draggable hovers over it
- [ ] Order change is saved to the data source without a separate save button
- [ ] Keyboard-only reorder works with arrow keys
- [ ] Screen reader announces the item's new position after move
- [ ] Reorder works on a touch device

## Common Mistakes
- No touch support: Mobile users cannot reorder → implement touch event equivalents
- No keyboard alternative: Keyboard-only users are excluded → add arrow-key move support
- Saving order only on page leave: Refresh loses changes → persist immediately after each drop
- No drop placeholder: User cannot predict landing position → render a visual placeholder slot
