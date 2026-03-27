# Skill: Pre-Deployment

## When to Use
Before any production deployment.

## Steps
1. Run production build locally (`npm run build` or equivalent)
2. Start production server locally (`npm run preview` or equivalent)
3. Click through EVERY page/route manually
4. Check browser console for errors — must be ZERO
5. Check network tab for failed requests — must be ZERO
6. Verify all images load (no broken image icons)
7. Test on mobile viewport (320px) in browser devtools
8. Verify meta tags (title, description, OG tags) on every page
9. Verify favicon loads
10. Check Lighthouse score: aim for 90+ on all metrics

## Verification
- [ ] Production build completes without errors
- [ ] All pages load in production mode
- [ ] Zero console errors
- [ ] Zero failed network requests
- [ ] All images display correctly
- [ ] Mobile layout works at 320px
- [ ] Lighthouse performance ≥ 90

## Common Mistakes
- Deploying without testing production build: Dev mode hides errors
- Skipping mobile test: Mobile issues only appear in production
- Ignoring console warnings: Warnings become errors under load
