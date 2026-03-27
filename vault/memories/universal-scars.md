# Memory: Universal Scars

## Scars (mistakes to never repeat)

### Scar: Hardcoded colors
**When:** During the design system module
**What happened:** We hardcoded colors directly in component files instead of CSS variables
**Consequence:** Client wanted to adjust the blue tone — we had to find-and-replace across 23 files. Three got missed. Site looked broken for a day.
**Now we:** Every color goes through CSS custom properties. No exceptions. Not even borders or shadows.

### Scar: Console.log in production
**When:** During first deployment
**What happened:** We left console.log statements scattered through the codebase
**Consequence:** Client opened DevTools to show a friend and saw debug messages everywhere. Lost confidence in the entire build.
**Now we:** Zero console.log in committed code. We use a proper logger or remove entirely.

### Scar: Skipped QA
**When:** Starting module 3
**What happened:** We skipped QA on module 2 because everything "looked fine"
**Consequence:** Module 3 built on a broken responsive layout. Had to tear apart two modules to fix one CSS issue.
**Now we:** QA runs after EVERY module. A 2-minute check prevents a 2-hour fix.

### Scar: Placeholder text shipped
**When:** Final review
**What happened:** Left "Lorem ipsum" and "example@email.com" in several places
**Consequence:** Client saw it and lost confidence. Started double-checking everything. Trust damaged.
**Now we:** Zero placeholder text anywhere. Every visible string is real content.

### Scar: Desktop-first
**When:** Mobile testing
**What happened:** Built desktop-first, added mobile styles as afterthought
**Consequence:** Mobile was a mess of overrides and !important. Took longer to fix mobile than building the original desktop version.
**Now we:** Mobile-first CSS. Always. Start with 320px and scale up.

### Scar: Copy-pasted navigation
**When:** Adding the second page
**What happened:** Copy-pasted nav from page 1 instead of shared component
**Consequence:** Every nav change required editing every page. Missed one. Client noticed a dead link.
**Now we:** Navigation is a shared component from the start. Single source of truth.

### Scar: Inline style "quick fix"
**When:** When client asked for a color change
**What happened:** Used inline styles for "quick fixes"
**Consequence:** Inline styles overrode the design system. Color change only applied to half the elements.
**Now we:** Inline styles are forbidden. Always. Even for "just this one thing."
