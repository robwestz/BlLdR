# Memory: Next.js Projects

## Scars

### Scar: Mixed routing
**When:** Next.js setup
**What happened:** Mixed pages/ and app/ router patterns
**Consequence:** Routing unpredictable. Some pages server, others client. Debugging nightmare.
**Now we:** Pick ONE routing pattern (app/ preferred). Use consistently.

### Scar: Regular img tags
**When:** Image handling
**What happened:** Used <img> instead of next/image
**Consequence:** Unoptimized images. 8+ second mobile load. Lighthouse crashed.
**Now we:** Always next/image. Specify width/height. Priority for above-fold.

## Insights

### Insight: Static first
**When:** Performance optimization
**What worked:** Used static generation for all pages that don't need real-time data
**Why:** Zero server load for marketing pages. Near-instant load times.
**Apply:** Default to static. Only use SSR/ISR when data must be fresh.
