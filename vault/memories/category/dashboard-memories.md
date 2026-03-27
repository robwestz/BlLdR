# Memory: Dashboard Projects

## Scars (mistakes to never repeat)

### Scar: Sequential API calls on mount
**When:** Building the main analytics dashboard
**What happened:** Fetched 6 independent data sources sequentially inside a single `useEffect` on mount
**Consequence:** The page took 12 seconds to load. Users reported the dashboard as "broken" in 3 separate support tickets before we parallelized the calls and cut load time to 2.1 seconds.
**Now we:** All independent data fetches fire in parallel. `Promise.all` or parallel query hooks. Sequential fetches only when one depends on another.

### Scar: Charts with no empty state
**When:** Shipping the sales overview module before data was populated
**What happened:** Rendered chart components with empty datasets — axes appeared, bars did not
**Consequence:** 4 users filed support tickets asking if their data was lost. One client escalated to a call. A two-line empty state message would have prevented all of it.
**Now we:** Every chart has an explicit empty state with a message. Design the empty state before the populated state.

### Scar: Real-time updates without debouncing
**When:** Adding live user activity indicators to the dashboard
**What happened:** Each connected client polled via WebSocket and re-rendered on every event at 500ms intervals
**Consequence:** 40 simultaneous users caused 40 connections each pushing updates every 500ms. Server CPU hit 90%. Had to add debouncing and throttling in an emergency deploy.
**Now we:** Real-time updates are debounced client-side and throttled server-side before the first user sees them.

### Scar: Column configuration lost on refresh
**When:** Building the data table module
**What happened:** Column sort order and visibility were component state only — no persistence layer
**Consequence:** Users configured their ideal view, refreshed, and lost it every time. After 2 weeks, adoption of the column customization feature dropped to near zero.
**Now we:** Any user-configured view state persists to localStorage or user preferences on change. Users never lose their setup.

## Insights (approaches to replicate)

### Insight: Skeleton loaders that match final layout
**When:** Building the KPI cards section of an analytics dashboard
**What worked:** Skeleton placeholders had identical height, width, and grid position to the loaded cards
**Why:** Users reported the page felt "instant" despite 800ms API calls — zero layout shift on load eliminated the perception of waiting.
**Apply:** Build the skeleton before the component. Match dimensions exactly. No generic spinner where a layout skeleton can go.

### Insight: Virtualized lists for large tables
**When:** Rendering a transaction history table with 5,000 rows
**What worked:** Swapped a standard map-rendered table for a virtualized list component
**Why:** Render time dropped from 4 seconds to under 100ms. The DOM went from 5,000 nodes to ~20 visible ones.
**Apply:** Any table that could exceed 100 rows gets a virtualized renderer. Decide at design time, not after the performance complaint.
