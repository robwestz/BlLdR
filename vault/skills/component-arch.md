# Skill: UI Component Architecture

## When to Use
Before building any UI component that will be used in more than one place,
or any component complex enough to need internal state management.

## Steps
1. Define the component's single responsibility in one sentence
2. List all data it needs: what comes from props, what is internal state
3. Define the public interface (props): types, required vs optional, defaults
4. Identify variants: what configurations does this component support?
5. Identify states: loading, error, empty, populated — design each explicitly
6. Decide composition strategy:
   - Simple (one component, all logic inside): < 80 lines, single variant
   - Compound (parent + sub-components): multiple related pieces used together
   - Slot-based (children prop): when content varies but structure stays fixed
7. Write the prop interface before writing the render logic
8. Build the component in state order: render empty state first, then error, then loading, then populated

## Verification
- [ ] Component name is a noun, not a verb (Button, not HandleClick)
- [ ] Props interface covers every visible variation without any-typing
- [ ] All four states (loading, error, empty, populated) are handled
- [ ] Component is isolated: removing it doesn't break unrelated functionality
- [ ] No direct DOM queries inside the component (no getElementById)
- [ ] All interactive elements have accessible labels

## Common Mistakes
- Combining data fetching with display: Separate container from presentational logic
- Designing for one use case: Build for the interface contract, not the current user
- Skipping the empty state: "No items found" is always needed, always forgotten
- Prop drilling through 3+ levels: This signals the data should live higher or in context
