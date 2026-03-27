# Skill: Notification System

## When to Use
Informing the user about the outcome of an action or a background event without blocking their workflow.

## Steps
1. Place the toast container at top-right for desktop; bottom-center for mobile (above thumb reach)
2. Define four types: success, error, warning, info — each with a distinct icon and color
3. Set auto-dismiss timers: success → 3 seconds, warning/info → 5 seconds, error → 8 seconds or manual only
4. Add `role="alert"` and `aria-live="assertive"` on error toasts; `aria-live="polite"` on the rest
5. Stack multiple toasts vertically with newest on top; cap the visible stack at 3
6. Provide a close (×) button on every toast regardless of auto-dismiss
7. Pause auto-dismiss timer when the user hovers over or focuses the toast
8. Never use a toast for actions that require user confirmation — use a modal instead
9. Keep messages under 80 characters; link to details if more context is needed

## Verification
- [ ] Screen reader announces each toast when it appears
- [ ] Error toasts do not disappear without user action (or dismiss after 8s minimum)
- [ ] Hovering a toast pauses its dismiss countdown
- [ ] More than 3 simultaneous toasts: oldest are removed from the stack
- [ ] Every toast has a visible close button
- [ ] No toast is used for a destructive action requiring confirmation

## Common Mistakes
- Using toasts for confirmations: User may miss them → use a blocking modal for destructive actions
- Identical dismiss timing for all types: Errors need more time → use type-specific durations
- No aria-live region: Screen reader users never hear notifications → add aria-live to the container
- Auto-dismissing errors: User may not read in time → errors should require manual dismissal
