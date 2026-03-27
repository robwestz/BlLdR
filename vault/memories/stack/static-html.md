# Memory: Static HTML Projects

## Scars

### Scar: Duplicated header/footer
**When:** Multi-page site
**What happened:** Copied header and footer into every HTML file
**Consequence:** Changed nav link — had to edit 8 files. Missed 2. Client found broken links.
**Now we:** Use includes (template engine, build tool, or web components). Single source for shared elements.

## Insights

### Insight: CSS custom properties work everywhere
**When:** Theming
**What worked:** Used CSS custom properties for all design tokens, even without a framework
**Why:** One :root block controls the entire site. Theme changes are instant. Works in all browsers.
**Apply:** Define colors, fonts, spacing, radius as --custom-properties in :root.
