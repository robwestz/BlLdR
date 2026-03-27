# Skill: Performance Optimization

## When to Use
Before deployment or when load times exceed 3 seconds.

## Steps
1. Run Lighthouse in Chrome DevTools → note Performance score
2. Optimize images: use WebP/AVIF, set explicit width/height, lazy-load below fold
3. Minimize bundle: remove unused dependencies, use dynamic imports for heavy modules
4. Enable text compression (gzip/brotli) on the server
5. Set cache headers for static assets (CSS, JS, images)
6. Eliminate layout shifts: set dimensions on images, reserve space for dynamic content
7. Defer non-critical JS: use `async` or `defer` on script tags
8. Preload critical fonts: `<link rel="preload" as="font">`

## Verification
- [ ] Lighthouse Performance ≥ 90
- [ ] First Contentful Paint < 1.5s
- [ ] No layout shifts (CLS < 0.1)
- [ ] All images have explicit dimensions
- [ ] Bundle size < 200KB (gzipped, for typical sites)

## Common Mistakes
- Optimizing before measuring: Run Lighthouse FIRST, fix what it flags
- Uncompressed images: A single 5MB hero image ruins everything
- Loading all JS upfront: Split code by route, lazy-load heavy modules
