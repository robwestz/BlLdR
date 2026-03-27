# Constraint: Performance Requirements

## Scope
Always. All deployed code.

### ❌ Unoptimized images
**Banned:** Images > 500KB, images without explicit dimensions
**Why:** A single unoptimized image can make page load take 10+ seconds on mobile.
**Instead:** Compress to WebP/AVIF. Set width/height. Lazy-load below fold.

### ❌ Blocking resources
**Banned:** Large synchronous JS/CSS in `<head>` that blocks first paint
**Why:** User sees white screen for seconds. Bounce rate increases 30% per second.
**Instead:** Async/defer for non-critical JS. Inline critical CSS. Preload fonts.

### ❌ Uncontrolled bundle size
**Banned:** Frontend bundle > 300KB gzipped without justification
**Why:** Slow load, especially on mobile networks.
**Instead:** Code-split by route. Dynamic import for heavy features. Audit with bundleanalyzer.
