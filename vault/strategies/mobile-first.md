# Strategy: Mobile-First Development

## When to Apply
Any project where mobile users exist (almost always).

## The Approach

### Step 1: Design the mobile layout
At 320px width, what does the user see? Design this first.

### Step 2: Build the mobile version
Write CSS for the smallest screen. No media queries yet. This is the base.

### Step 3: Layer up
Add min-width media queries for wider screens:
If [≥640px] → 2-column layouts, larger spacing
If [≥768px] → sidebar navigation, expanded cards
If [≥1024px] → full desktop layout, max-width container

### Step 4: Test at each breakpoint
After every visual change, verify at 320px, 768px, and 1024px.

## Traps to Avoid
- Adding max-width queries to "fix mobile": This means you built desktop-first. Start over with min-width.
- Hiding content on mobile: Restructure the layout, don't display:none critical content.
