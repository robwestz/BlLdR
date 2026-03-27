# Design Derivation Reference

How the Forge engine derives a design system from human-language answers.

## Input → Output

| Human Input | Derived Output |
|-------------|---------------|
| Feeling: "professional" | Neutral palette, serif headings, generous whitespace |
| Feeling: "playful" | Bright accent colors, rounded corners, bouncy transitions |
| Feeling: "minimal" | Monochrome palette, system fonts, tight spacing |
| Feeling: "luxurious" | Dark backgrounds, gold accents, large typography |
| Color hint: "blue-ish, ocean" | Primary: #0077B6, shades derived from ocean palette |
| Color hint: "warm, earthy" | Primary: #B07D62, earth tone palette |
| Color hint: "brand color #FF6B35" | Primary: #FF6B35, complementary palette derived |

## Derivation Chain

```
Feeling → Mood Board → Palette Type → Color Variables
  ↓
Typography scale (feeling maps to font pairing)
  ↓
Spacing scale (feeling maps to density)
  ↓
Component style (border-radius, shadows, transitions)
  ↓
Complete SYSTEM.md design tokens
```

## Palette Derivation

| Mood | Primary Range | Background | Text | Accent Strategy |
|------|--------------|------------|------|-----------------|
| Professional | Cool neutrals (slate, gray, navy) | Light (#FAFAFA) | Dark (#1A1A1A) | Single accent, muted |
| Playful | Warm brights (coral, teal, violet) | White or tinted | Dark | Multiple accents OK |
| Minimal | Monochrome (black, white, one gray) | White | Black | No accent or single muted |
| Luxurious | Deep darks (charcoal, navy, forest) | Dark (#0A0A0A) | Light (#F5F5F5) | Metallic or warm accent |
| Technical | Cool blues (slate, indigo) | Dark or light | High contrast | Neon or bright accent |

## Typography Derivation

| Mood | Heading Font | Body Font | Scale Ratio |
|------|-------------|-----------|-------------|
| Professional | Serif (Playfair, Lora) | Sans (Inter, Source Sans) | 1.25 (major third) |
| Playful | Rounded sans (Nunito, Poppins) | Same family | 1.2 (minor third) |
| Minimal | System sans (system-ui) | Same | 1.125 (major second) |
| Luxurious | Display serif (Cormorant) | Light sans (Jost) | 1.333 (perfect fourth) |
| Technical | Monospace (JetBrains Mono) | Sans (Inter) | 1.25 (major third) |

## Spacing Derivation

| Mood | Base Unit | Density | Border Radius |
|------|-----------|---------|---------------|
| Professional | 8px | Normal (1x) | 4-8px |
| Playful | 8px | Relaxed (1.25x) | 12-16px |
| Minimal | 4px | Tight (0.75x) | 0-2px |
| Luxurious | 8px | Generous (1.5x) | 0-4px |
| Technical | 4px | Compact (0.875x) | 4px |

## Location-Based Adjustments

| Signal | Adjustment |
|--------|-----------|
| Africa / Middle East | Lighter assets, mobile-first, WhatsApp integration |
| Sweden | Swish payment default, Swedish UI language |
| Global / English | Stripe payment default, English UI |
| Tourist audience | Large touch targets (48px min), simple navigation |
| B2B audience | Dense information, desktop-optimized |
