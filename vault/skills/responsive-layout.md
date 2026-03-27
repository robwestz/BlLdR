# Skill: Responsive Layout

## When to Use
Building any visual interface that must work across screen sizes.

## Steps
1. Start with mobile layout (320px). Design this FIRST.
2. Add content and components for mobile. Ensure everything fits.
3. Add `sm` breakpoint (640px): adjust spacing, maybe 2-column grid
4. Add `md` breakpoint (768px): sidebar appears, grid expands
5. Add `lg` breakpoint (1024px): full desktop layout
6. Set max-width container (1200-1440px) to prevent ultra-wide stretching
7. Test touch targets: minimum 44×44px for all interactive elements
8. Test text readability: minimum 16px body text, adequate line-height

## Verification
- [ ] Layout works at 320px without horizontal scroll
- [ ] Layout works at 768px with appropriate adaptation
- [ ] Layout works at 1024px with full desktop features
- [ ] No text smaller than 16px on mobile
- [ ] All buttons/links are at least 44×44px touch target
- [ ] Images scale without overflow or distortion

## Common Mistakes
- Desktop-first then "fix mobile": Always mobile-first CSS
- Fixed pixel widths: Use relative units (%, rem, vw) and max-width
- Hiding content on mobile with display:none: Restructure, don't hide
