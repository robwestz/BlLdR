# Skill: Dark Mode

## When to Use
Any web UI that should respect user color-scheme preference or offer a manual theme toggle.

## Steps
1. Define all colors as CSS custom properties on `:root` — never hardcode color values inside components
2. Create a `[data-theme="dark"]` selector on `<html>` that overrides every color variable
3. On initial page load (before first paint): read `localStorage.getItem("theme")`, fall back to `prefers-color-scheme`, then set `data-theme` on `<html>` via an inline `<script>` in `<head>` — this prevents flash
4. Render a toggle button with a sun icon in dark mode and a moon icon in light mode
5. On toggle click: flip `data-theme` on `<html>` and write the new value to `localStorage`
6. Never use `prefers-color-scheme` alone without a manual override — always let the user win
7. Verify that images, SVGs, and third-party embeds remain legible in both themes
8. Test all interactive states (hover, focus, disabled) in both themes — define those as variables too

## Verification
- [ ] Hard refresh on a previously toggled theme loads the correct theme with no visible flash
- [ ] Toggle button icon matches the current theme (sun = dark mode active, moon = light mode active)
- [ ] All text meets WCAG AA contrast ratio (4.5:1) in both themes
- [ ] No color is hardcoded in any component stylesheet — all come from CSS variables
- [ ] System dark mode preference is respected when no localStorage value exists
- [ ] Changing the OS preference while the tab is open updates the theme (if no manual override is set)

## Common Mistakes
- Setting theme in JS after React/framework hydration: Causes flash of wrong theme → use inline script in `<head>` before any framework runs
- Hardcoding colors in components: Component breaks when variables change → use CSS variables exclusively
- Ignoring `prefers-color-scheme`: First-time visitors get light mode regardless of OS setting → always check media query as fallback
- Only toggling background and text: Borders, shadows, and icons break → define variables for every visual token
