# Memory: React + Vite Projects

## Scars

### Scar: Redux for simple state
**When:** State management
**What happened:** Reached for Redux before the app had complex state
**Consequence:** Massive boilerplate for form state. Every developer confused.
**Now we:** useState and useContext first. Add state library only when prop drilling is proven painful.

## Insights

### Insight: Vite speed
**When:** Development workflow
**What worked:** Vite's hot reload was near-instant, enabling rapid iteration
**Why:** Feedback loop under 200ms means more experiments per hour.
**Apply:** Don't add middleware or plugins that slow Vite's HMR. Keep config minimal.
