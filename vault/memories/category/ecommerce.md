# Memory: E-Commerce Projects

## Scars

### Scar: Cart lost on refresh
**When:** Shopping cart
**What happened:** Cart state only in React state, not persisted
**Consequence:** User added 5 items, refreshed, everything gone. They left.
**Now we:** Cart persists to localStorage or session. Refresh preserves cart.

## Insights

### Insight: Product card hierarchy
**When:** Product display
**What worked:** Large image, minimal text, clear price, one CTA button
**Why:** Users scanned quickly. Clear hierarchy converted well.
**Apply:** Product cards: 60% image, 20% text, 20% action. Price never hidden.
