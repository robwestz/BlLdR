# Strategy: When to Cache

## When to Apply
When considering whether to add caching to improve performance or reduce load.

## The Approach

### Step 1: Measure First
Is this actually slow? Get a real number. Do not cache based on assumption.
What is the current response time? What is the acceptable threshold?

### Step 2: Assess the Data
- How often does this data change?
- Is staleness acceptable — and for how long?
- Is this data user-specific or shared across users?

### Step 3: Define Invalidation Before Writing the Cache
What triggers a cache bust? How will stale data be evicted?
If you cannot answer this clearly, the cache is not ready to implement.

### Step 4: Choose the Layer
- In-memory: fastest, lost on restart, single instance only.
- HTTP cache headers: free for GET requests, no infrastructure needed.
- Shared cache (e.g. Redis): spans instances, requires operational overhead.

## Decision Points
If response time is under 200ms → no cache needed, solve other problems first.
If data changes more than once per second → caching adds complexity without gain.
If invalidation requires business logic → document it fully before implementing.
If the data is user-specific → do not cache it in a shared layer.

## Traps to Avoid
- Caching without an invalidation plan: A cache without expiry is a bug waiting to surface.
- Caching mutable user-specific data globally: Leads to users seeing each other's data.
- "We'll add caching later": The architecture must support it from the start or retrofitting costs double.
