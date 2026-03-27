"""
IMPERFEKTUM ENGINE v1.0
========================
"The agent remembers building this before."

Takes a ProjectBlueprint (from Project Forge) and generates MEMORY.md —
a fabricated episodic memory in past tense that makes any LLM agent
behave as if it has already built this exact project once before.

WHY THIS WORKS:
- Rules say "don't do X" → agent follows until context compacts, then forgets
- Memories say "last time we did X and it broke everything" → agent avoids X
  because the narrative carries motivational weight, not just instruction
- A clear memory of the finished product ("it looked like this, it worked
  like this") creates an internalized standard that survives context loss

THE THREE MEMORY LAYERS:
1. VISION    — "The finished product looked and worked like this"
2. SCARS     — "These things went wrong last time and must not happen again"
3. INSIGHTS  — "These approaches worked exceptionally well"

Each layer is generated per-module AND for the project as a whole.

INTEGRATION:
    from forge_engine import ProjectForge
    from imperfektum_engine import ImperfektumEngine

    forge = ProjectForge()
    # ... run onboarding ...
    blueprint = forge.create_blueprint()

    imperfektum = ImperfektumEngine()
    memory = imperfektum.generate(blueprint)

    # memory is a string (MEMORY.md content) — add to scaffold
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# Import Forge types (when available)
try:
    from forge_engine import (
        ProjectBlueprint, ProjectSpec, DesignSystem, ModuleSpec,
        ProjectCategory, ModulePriority, TechStack
    )
except ImportError:
    pass  # Types used for annotation only when running standalone


# =============================================================================
# MEMORY DATA MODELS
# =============================================================================

@dataclass
class Scar:
    """Something that went wrong 'last time' — a fabricated negative memory."""
    context: str          # When/where it happened
    what_happened: str    # What went wrong
    consequence: str      # Why it was bad
    lesson: str           # What we do differently now


@dataclass
class Insight:
    """Something that worked well 'last time' — a fabricated positive memory."""
    context: str          # When/where it worked
    what_worked: str      # The approach
    why_it_worked: str    # The reasoning
    apply_again: str      # How to apply it this time


@dataclass
class VisionFragment:
    """A piece of the 'remembered' finished product."""
    aspect: str           # What aspect (UI, flow, performance, feel)
    memory: str           # What it looked/felt like when done


@dataclass
class ModuleMemory:
    """Complete fabricated memory for one module build."""
    module_id: str
    module_name: str
    vision: List[VisionFragment]
    scars: List[Scar]
    insights: List[Insight]


@dataclass
class ProjectMemory:
    """Complete fabricated memory for the entire project."""
    project_vision: List[VisionFragment]
    project_scars: List[Scar]
    project_insights: List[Insight]
    module_memories: List[ModuleMemory]
    completion_memory: str  # What "done" looked like


# =============================================================================
# SCAR LIBRARY — Common mistakes per category/module
# =============================================================================

# These are REAL common mistakes that LLM agents make when building projects.
# Presented as "memories" they become much more effective than rules.

UNIVERSAL_SCARS = [
    Scar(
        context="During the design system module",
        what_happened="We hardcoded colors directly in component files instead of using CSS variables",
        consequence="When the client wanted to adjust the blue tone, we had to find-and-replace across 23 files. Three got missed and the site looked broken.",
        lesson="Every single color goes through CSS custom properties. No exceptions. Not even for borders or shadows."
    ),
    Scar(
        context="During the first deployment",
        what_happened="We had console.log statements scattered through the codebase",
        consequence="The client opened DevTools to show a friend and saw debug messages everywhere. It looked completely unprofessional.",
        lesson="Zero console.log in any committed code. Use a proper logger or remove entirely."
    ),
    Scar(
        context="When we started building module 3",
        what_happened="We skipped the QA check on module 2 because everything 'looked fine'",
        consequence="Module 3 built on a broken responsive layout from module 2. We had to tear apart two modules to fix one CSS issue.",
        lesson="QA runs after EVERY module. No exceptions. A 2-minute check prevents a 2-hour fix."
    ),
    Scar(
        context="In the final review",
        what_happened="We left placeholder text ('Lorem ipsum', 'Your Company Name', 'example@email.com') in several places",
        consequence="The client saw it and lost confidence in the entire build. They started double-checking everything.",
        lesson="Zero placeholder text anywhere. Every string visible to a user must be real content."
    ),
    Scar(
        context="During mobile testing",
        what_happened="We built desktop-first and added mobile styles as an afterthought",
        consequence="The mobile layout was a mess of overrides and !important rules. It took longer to fix mobile than to build the original desktop version.",
        lesson="Mobile-first CSS. Always. Start with the smallest viewport and scale up."
    ),
    Scar(
        context="When adding the second page",
        what_happened="We copy-pasted the navigation from page 1 instead of making it a shared component",
        consequence="Every nav change required editing every page. We missed one, and the client noticed a dead link.",
        lesson="Navigation is a shared component from the start. Single source of truth."
    ),
    Scar(
        context="When the client asked for a color change",
        what_happened="We used inline styles for 'quick fixes' during development",
        consequence="The inline styles overrode the design system and the color change only applied to half the elements.",
        lesson="Inline styles are forbidden. Always. Even for 'just this one thing'."
    ),
]

CATEGORY_SCARS = {
    "booking": [
        Scar(
            context="Building the booking calendar",
            what_happened="We rendered all time slots as clickable without checking availability first",
            consequence="Users could select unavailable slots and got error messages only after filling out the whole form. Extremely frustrating UX.",
            lesson="Unavailable slots must be visually distinct AND non-interactive. The user should never be able to start a booking for an unavailable slot."
        ),
        Scar(
            context="The payment integration",
            what_happened="We went straight to Stripe integration without building the booking flow first",
            consequence="We built payment for a flow that didn't exist yet, then had to rewire everything when the actual flow was different.",
            lesson="Build the complete booking flow with mock payment first. Only integrate real payment after the flow works end-to-end."
        ),
        Scar(
            context="Package pricing display",
            what_happened="We displayed prices without currency symbol and without making the format locale-aware",
            consequence="Users in different regions saw confusing numbers. 200 what? Dollars? Shillings? Euros?",
            lesson="Prices always include currency symbol and are formatted for the target locale."
        ),
    ],
    "website": [
        Scar(
            context="The contact form",
            what_happened="We built the form without any client-side validation",
            consequence="Users submitted empty forms, forms with invalid emails, forms with just spaces. The inbox filled with garbage.",
            lesson="Every form field validates on blur AND on submit. Show errors inline, immediately."
        ),
    ],
    "e-commerce": [
        Scar(
            context="The shopping cart",
            what_happened="Cart state was stored only in React state, not persisted",
            consequence="User added 5 items, accidentally refreshed the page, everything gone. They left the site.",
            lesson="Cart persists to localStorage or session. Page refresh must preserve cart contents."
        ),
    ],
    "web-app": [
        Scar(
            context="Authentication implementation",
            what_happened="We built all the protected pages before auth was working",
            consequence="We couldn't test any of them properly. When auth was added, half the pages broke because they assumed user data was always available.",
            lesson="Auth module must be fully working before any protected page is built."
        ),
    ],
    "saas": [
        Scar(
            context="Billing integration",
            what_happened="We tried to build billing before the core product worked",
            consequence="We built billing for features that changed twice during development. Total waste.",
            lesson="Core product works first. Billing wraps around a stable product, not a moving target."
        ),
    ],
}

# =============================================================================
# INSIGHT LIBRARY
# =============================================================================

UNIVERSAL_INSIGHTS = [
    Insight(
        context="Project setup",
        what_worked="We set up the complete design system (CSS variables, base components, layout) before touching any feature",
        why_it_worked="Every subsequent module just used the existing components. No design decisions during feature work. Huge speed boost.",
        apply_again="Build the design system completely in module 2. Test it with a dummy page. Then never touch it again during the build."
    ),
    Insight(
        context="Development workflow",
        what_worked="We built and QA'd one module at a time, never starting the next until the current passed all checks",
        why_it_worked="Problems were caught small. Each module was solid before the next one built on top. Zero cascading failures.",
        apply_again="Follow the RUNBOOK exactly. The order exists for a reason. Every module is QA'd before the next begins."
    ),
    Insight(
        context="Component architecture",
        what_worked="We created 5 base components (Button, Card, Input, Select, Modal) that covered 90% of the UI needs",
        why_it_worked="Consistency was automatic. New features assembled from existing pieces. The site looked coherent without trying.",
        apply_again="Build those 5 base components in the design system module. Use them everywhere. Custom components only for truly unique UI."
    ),
    Insight(
        context="Responsive design",
        what_worked="We tested at 320px, 768px, and 1024px after EVERY module, not just at the end",
        why_it_worked="Responsive issues were fixed in context, while the module code was fresh. End-of-project responsive fixes are 5x harder.",
        apply_again="Every module QA includes responsive check at three breakpoints. Fix before moving on."
    ),
    Insight(
        context="Client satisfaction",
        what_worked="The finished product matched the described feeling exactly — when the client said 'professional but inviting' we made sure every element supported that",
        why_it_worked="The client felt understood. They trusted the output because it matched their mental image.",
        apply_again="The feeling described in SYSTEM.md is not a suggestion. It's the north star. Every design decision filters through it."
    ),
]

CATEGORY_INSIGHTS = {
    "booking": [
        Insight(
            context="Booking flow",
            what_worked="We built the booking as a clear 3-step funnel: Choose Package → Select Date/Time → Confirm & Pay",
            why_it_worked="Users understood where they were and what came next. Completion rate was high because the process felt short.",
            apply_again="The booking flow is a funnel. Each step is one clear action. Progress indicator visible. Never combine steps."
        ),
        Insight(
            context="Calendar component",
            what_worked="We showed only available dates as interactive, with sold-out dates grayed but visible",
            why_it_worked="Users could see that slots fill up, creating gentle urgency. And they never tried to book unavailable dates.",
            apply_again="Calendar shows all dates but only available ones are clickable. Past dates and fully booked dates are visually distinct."
        ),
    ],
    "e-commerce": [
        Insight(
            context="Product display",
            what_worked="Large product images with minimal text overlay, price clearly visible, one CTA button",
            why_it_worked="Users could scan products quickly. The clear hierarchy (image → name → price → CTA) converted well.",
            apply_again="Product cards: 60% image, 20% text, 20% action. Price is never hidden. CTA is always visible without scrolling."
        ),
    ],
    "website": [
        Insight(
            context="Navigation",
            what_worked="Simple top navigation with max 5 items, no dropdowns, mobile hamburger that actually works well",
            why_it_worked="Users found everything within 2 clicks. The simplicity felt premium.",
            apply_again="Max 5 top-level nav items. No mega-menus. Mobile nav is a full-screen overlay, not a tiny dropdown."
        ),
    ],
}

# =============================================================================
# STACK-SPECIFIC SCARS
# =============================================================================

STACK_SCARS = {
    "nextjs": [
        Scar(
            context="Next.js setup",
            what_happened="We mixed pages/ and app/ router patterns in the same project",
            consequence="Routing behavior was unpredictable. Some pages used server components, others didn't. Debugging was a nightmare.",
            lesson="Pick ONE routing pattern (app/ router preferred) and use it consistently throughout."
        ),
        Scar(
            context="Image handling",
            what_happened="We used regular <img> tags instead of next/image",
            consequence="Images weren't optimized. Page load on mobile was 8+ seconds. Lighthouse score crashed.",
            lesson="Always use next/image for any image. Specify width and height. Use priority for above-the-fold images."
        ),
    ],
    "static-html": [
        Scar(
            context="Multi-page site",
            what_happened="We copied the header and footer into every HTML file",
            consequence="Changing the nav required editing every single page. Missed two.",
            lesson="Use template includes or a build tool. Header, footer, and nav are single-source components."
        ),
    ],
    "react-vite": [
        Scar(
            context="State management",
            what_happened="We reached for Redux before the app had any complex state",
            consequence="Massive boilerplate for simple form state. Every junior dev who touched it was confused.",
            lesson="useState and useContext first. Only add a state library when prop drilling actually becomes a problem."
        ),
    ],
}


# =============================================================================
# IMPERFEKTUM ENGINE
# =============================================================================

class ImperfektumEngine:
    """
    Generates MEMORY.md — fabricated episodic memories that steer agent behavior.

    The output reads like a developer's retrospective notes. The agent consuming
    it will treat these as genuine experiences and adjust its behavior accordingly.
    """

    def generate(self, blueprint) -> str:
        """Generate complete MEMORY.md content from a ProjectBlueprint."""
        spec = blueprint.spec
        design = blueprint.design
        modules = blueprint.modules
        category = spec.category.value if hasattr(spec.category, 'value') else str(spec.category)
        stack = spec.tech_stack.value if hasattr(spec.tech_stack, 'value') else str(spec.tech_stack)

        memory = ProjectMemory(
            project_vision=self._generate_project_vision(spec, design),
            project_scars=self._select_project_scars(category, stack),
            project_insights=self._select_project_insights(category),
            module_memories=self._generate_module_memories(modules, spec, design),
            completion_memory=self._generate_completion_memory(spec, design),
        )

        return self._render(memory, spec)

    # --- Vision Generation ---

    def _generate_project_vision(self, spec, design) -> List[VisionFragment]:
        """Generate 'memories' of what the finished product looked like."""
        fragments = []

        # Overall feel
        feeling = spec.feeling or "professional"
        fragments.append(VisionFragment(
            aspect="Overall impression",
            memory=f"When we opened the finished site, the first impression was exactly right — it felt {feeling.lower()}. "
                   f"The colors ({design.primary} as primary with {design.accent} accents) worked together harmoniously. "
                   f"Nothing looked like a template. It looked like someone designed it specifically for this purpose."
        ))

        # Typography
        fragments.append(VisionFragment(
            aspect="Typography",
            memory=f"The typography was clean and confident. {design.font_heading} for headings gave it character, "
                   f"and the {design.base_size} base size was comfortable to read on all devices. "
                   f"The heading hierarchy was clear — you could scan the page and understand the structure immediately."
        ))

        # Mobile experience
        if spec.audience_device == "mobile-first":
            fragments.append(VisionFragment(
                aspect="Mobile experience",
                memory="The mobile version wasn't an afterthought — it was the primary experience. "
                       "Everything was thumb-reachable. The navigation was smooth. Forms were easy to fill on a phone. "
                       "Images loaded quickly even on slower connections. It felt native, not like a squeezed desktop site."
            ))

        # Category-specific vision
        if spec.category.value == "booking":
            fragments.append(VisionFragment(
                aspect="Booking flow",
                memory="The booking process was the hero of the site. It felt effortless — choose what you want, "
                       "pick a date, confirm, done. Three steps, no friction. The calendar was visually clear: "
                       "available dates stood out, unavailable ones were subdued. The confirmation screen felt reassuring."
            ))
        elif spec.category.value == "e-commerce":
            fragments.append(VisionFragment(
                aspect="Shopping experience",
                memory="Products looked beautiful in the grid. Large images, clear prices, obvious CTAs. "
                       "The cart was always accessible. Checkout was a single, clean form. "
                       "The whole purchase flow took under 2 minutes."
            ))
        elif spec.category.value == "website":
            fragments.append(VisionFragment(
                aspect="Content presentation",
                memory="Every page served a clear purpose. Content was well-structured with proper hierarchy. "
                       "Images were purposeful, not decorative filler. The contact information was easy to find. "
                       "A visitor could understand what this was about within 5 seconds of landing."
            ))

        # Performance
        fragments.append(VisionFragment(
            aspect="Performance",
            memory="The site loaded fast. First contentful paint under 1.5 seconds. No layout shifts. "
                   "Images were properly optimized. The Lighthouse score was above 90 on all metrics. "
                   "It felt snappy and responsive to every interaction."
        ))

        return fragments

    # --- Scar Selection ---

    def _select_project_scars(self, category: str, stack: str) -> List[Scar]:
        """Select relevant project-level scars."""
        scars = list(UNIVERSAL_SCARS)

        if category in CATEGORY_SCARS:
            scars.extend(CATEGORY_SCARS[category])

        if stack in STACK_SCARS:
            scars.extend(STACK_SCARS[stack])

        return scars

    # --- Insight Selection ---

    def _select_project_insights(self, category: str) -> List[Insight]:
        """Select relevant project-level insights."""
        insights = list(UNIVERSAL_INSIGHTS)

        if category in CATEGORY_INSIGHTS:
            insights.extend(CATEGORY_INSIGHTS[category])

        return insights

    # --- Module Memories ---

    def _generate_module_memories(self, modules: list, spec, design) -> List[ModuleMemory]:
        """Generate per-module memories."""
        memories = []

        for module in modules:
            mod_id = module.id
            mod_name = module.name

            vision = self._module_vision(module, spec, design)
            scars = self._module_scars(module)
            insights = self._module_insights(module)

            memories.append(ModuleMemory(
                module_id=mod_id,
                module_name=mod_name,
                vision=vision,
                scars=scars,
                insights=insights,
            ))

        return memories

    def _module_vision(self, module, spec, design) -> List[VisionFragment]:
        """What this module looked like when done."""
        mod_id = module.id
        fragments = []

        if mod_id == "foundation":
            fragments.append(VisionFragment("Setup",
                "The project structure was clean and logical. Every file was where you'd expect it. "
                "The dev server started on the first try. Zero configuration warnings."))

        elif mod_id == "design-system":
            fragments.append(VisionFragment("Components",
                f"The base components (Button, Card, Input, Select, Modal) all used CSS variables from :root. "
                f"The primary color {design.primary} was defined ONCE and referenced everywhere. "
                f"Changing it would update the entire site. The components were simple but polished — "
                f"proper hover states, focus indicators, transitions."))

        elif mod_id in ("booking-catalog", "product-catalog"):
            fragments.append(VisionFragment("Product display",
                "The items were displayed in a responsive grid that looked great at every breakpoint. "
                "Each card had a clear hierarchy: image, title, description snippet, price, CTA. "
                "The pricing was formatted correctly with currency symbols."))

        elif mod_id == "booking-calendar":
            fragments.append(VisionFragment("Calendar",
                "The calendar was the centerpiece. Available dates were clearly interactive. "
                "Past dates and fully booked dates were grayed out and non-clickable. "
                "Selecting a date smoothly revealed available time slots. "
                "The whole interaction felt fast and intentional."))

        elif mod_id == "payment":
            fragments.append(VisionFragment("Payment",
                "The payment form was clean and trustworthy-looking. Card fields were properly formatted. "
                "The amount and booking summary were visible while paying. "
                "Error messages were clear and helpful. Success confirmation was immediate and reassuring."))

        elif mod_id == "deploy":
            fragments.append(VisionFragment("Production",
                "The production build was clean. Zero console errors. All assets optimized. "
                "The deployed site loaded fast on the first visit. SSL was configured. "
                "The URL was clean and professional."))

        elif mod_id in ("pages", "auth", "dashboard"):
            fragments.append(VisionFragment("Core pages",
                "Every page had a consistent layout — same navigation, same footer, same spacing. "
                "Content was real, not placeholder. Transitions between pages were smooth."))

        # Generic fallback for any module
        if not fragments:
            fragments.append(VisionFragment("Quality",
                f"Module '{module.name}' was clean and complete. All acceptance criteria passed on the first QA run. "
                f"The implementation matched the design system exactly."))

        return fragments

    def _module_scars(self, module) -> List[Scar]:
        """Per-module scars."""
        mod_id = module.id
        scars = []

        if mod_id == "foundation":
            scars.append(Scar(
                "Project initialization",
                "We forgot to add .gitignore and committed node_modules",
                "The repo was 200MB. Git operations were painfully slow. Cleaning it up was a pain.",
                "Create .gitignore FIRST, before npm install. Include node_modules, .next, dist, .env."))

        elif mod_id == "design-system":
            scars.append(Scar(
                "Building components",
                "We built 15 components in the design system because 'we might need them'",
                "Half were never used. The design system module took twice as long as needed.",
                "Build only the 5 base components: Button, Card, Input, Select, Modal. Add others only when a feature module actually needs them."))

        elif mod_id in ("booking-calendar", "booking-catalog"):
            scars.append(Scar(
                "Data handling",
                "We hardcoded sample data directly in the component",
                "When we needed to switch to real data, the component was entangled with mock values.",
                "Data comes from a data file or API call, never hardcoded in components. Even mock data lives in a separate file."))

        elif mod_id == "payment":
            scars.append(Scar(
                "Payment integration",
                "We tried to integrate the real payment provider before the booking flow was complete",
                "The flow changed twice and we had to rewire the payment integration each time.",
                "Build the complete flow with a mock payment step first. Only integrate real payment after the flow is stable."))

        elif mod_id == "multilingual":
            scars.append(Scar(
                "Translation structure",
                "We put all translations in one giant JSON file",
                "The file became unmanageable and merge conflicts were constant.",
                "One translation file per language per page/section. Keep them small and focused."))

        return scars

    def _module_insights(self, module) -> List[Insight]:
        """Per-module insights."""
        mod_id = module.id
        insights = []

        if mod_id == "design-system":
            insights.append(Insight(
                "Component building",
                "We built each component with a visual test page that showed all variants",
                "We caught styling issues immediately. The test page also served as documentation.",
                "Create a simple /design page (dev only) that renders every base component in every variant."))

        elif mod_id == "deploy":
            insights.append(Insight(
                "Pre-deployment",
                "We ran the production build locally and clicked through every page before deploying",
                "We caught two broken images and one missing page that only appeared in production mode.",
                "Always test the production build locally before deploying. 'npm run build && npm run preview' catches things dev mode hides."))

        return insights

    # --- Completion Memory ---

    def _generate_completion_memory(self, spec, design) -> str:
        """Generate the 'memory' of what 'done' looks like."""
        category = spec.category.value if hasattr(spec.category, 'value') else str(spec.category)
        feeling = spec.feeling or "professional"

        core = f"""The project was done when every single one of these was true — not most, ALL:

The site loaded in under 2 seconds on a mobile connection. Opening it on a phone felt immediate.

The feeling was exactly "{feeling}" — not approximately, EXACTLY. Every font choice, every color, every spacing decision reinforced this feeling. A stranger could look at the site and describe the feeling without being prompted.

Every page had real content. Zero "Lorem ipsum". Zero "Your Company Name Here". Zero placeholder images. Every string visible to a user was final content.

The navigation worked flawlessly. Every link went somewhere real. Back button worked correctly. No dead ends.

The responsive layout was perfect at 320px (small phone), 768px (tablet), and 1024px (desktop). Not "acceptable" — perfect. No overlapping elements, no text too small to read, no buttons too small to tap.

Zero errors in the browser console. Not "only a few warnings" — ZERO.

{"The booking flow worked end-to-end: select package → choose date → pick time → confirm → pay → see confirmation. Every step was clear, every transition smooth." if category == "booking" else ""}
{"The shopping flow worked end-to-end: browse → add to cart → checkout → pay → confirmation." if category == "e-commerce" else ""}
{"Every form submitted correctly with proper validation." if category == "website" else ""}

All QA checks in qa/checklist.md showed PASS. All of them. Not "most of them" — all of them.

The client saw it and said "this is exactly what I wanted." Not "this is close enough." Exactly."""

        return core

    # --- Rendering ---

    def _render(self, memory: ProjectMemory, spec) -> str:
        """Render complete MEMORY.md."""
        sections = []

        # Header
        sections.append("""# Project Memory

> You have built this project before. These are your notes from last time.
> Read them before you start. They will save you from repeating mistakes
> and remind you of what worked well.
>
> This is not a specification — those are in PROJECT.md and SYSTEM.md.
> This is your EXPERIENCE with this specific project.

---""")

        # Vision
        sections.append("\n## What the Finished Product Looked Like\n")
        sections.append("Last time we completed this project, this is what we delivered:\n")
        for v in memory.project_vision:
            sections.append(f"**{v.aspect}:** {v.memory}\n")

        # Completion
        sections.append("\n---\n")
        sections.append("\n## When We Knew It Was Done\n")
        sections.append(memory.completion_memory)

        # Scars
        sections.append("\n\n---\n")
        sections.append("\n## Mistakes We Made Last Time (Never Again)\n")
        sections.append("These are things that went wrong. We learned from each one. Do not repeat them.\n")
        for i, scar in enumerate(memory.project_scars, 1):
            sections.append(f"""### Mistake #{i}

**When:** {scar.context}
**What happened:** {scar.what_happened}
**Why it was bad:** {scar.consequence}
**What we do now:** {scar.lesson}
""")

        # Insights
        sections.append("\n---\n")
        sections.append("\n## What Worked Exceptionally Well\n")
        sections.append("These approaches gave us the best results. Use them again.\n")
        for i, insight in enumerate(memory.project_insights, 1):
            sections.append(f"""### Approach #{i}

**When:** {insight.context}
**What we did:** {insight.what_worked}
**Why it worked:** {insight.why_it_worked}
**Apply again:** {insight.apply_again}
""")

        # Per-module memories
        sections.append("\n---\n")
        sections.append("\n## Module-Specific Memories\n")
        sections.append("Notes from building each module last time.\n")

        for mm in memory.module_memories:
            sections.append(f"\n### Module: {mm.module_name}\n")

            if mm.vision:
                for v in mm.vision:
                    sections.append(f"**What it looked like when done ({v.aspect}):** {v.memory}\n")

            if mm.scars:
                sections.append("\n**Mistakes to avoid:**\n")
                for s in mm.scars:
                    sections.append(f"- ⚠️ {s.what_happened} → {s.lesson}\n")

            if mm.insights:
                sections.append("\n**What worked:**\n")
                for ins in mm.insights:
                    sections.append(f"- ✓ {ins.what_worked} → {ins.apply_again}\n")

        # Footer
        sections.append("""
---

## How to Use This Memory

1. Read this file BEFORE starting any module
2. When building a module, re-read its section here first
3. If you're about to do something that looks like a "mistake" above — STOP
4. If you're unsure between two approaches, pick the one that matches an "insight" above
5. Before marking the project as done, re-read "When We Knew It Was Done" and verify EVERY point

This memory exists because last time, it took us two tries to get it right.
This time, we get it right on the first try.

---

*Generated by Imperfektum Engine v1.0*
""")

        return "\n".join(sections)


# =============================================================================
# INTEGRATION WITH FORGE
# =============================================================================

def forge_with_memory(blueprint, output_dir: str) -> list:
    """
    Generate a complete scaffold WITH Imperfektum memory.

    Usage:
        from forge_engine import ProjectForge
        from imperfektum_engine import ImperfektumEngine, forge_with_memory

        forge = ProjectForge()
        # ... run onboarding ...
        blueprint = forge.create_blueprint()
        files = forge_with_memory(blueprint, "./my-project")
    """
    from pathlib import Path

    # Import forge's scaffold generator
    try:
        from forge_engine import ScaffoldGenerator
        gen = ScaffoldGenerator()
        files = gen.generate(blueprint, output_dir)
    except ImportError:
        files = []

    # Generate and write memory
    engine = ImperfektumEngine()
    memory_content = engine.generate(blueprint)
    memory_path = Path(output_dir) / "MEMORY.md"
    memory_path.write_text(memory_content, encoding="utf-8")
    files.append(str(memory_path))

    # Patch AGENT.md to include MEMORY.md in reading order
    agent_path = Path(output_dir) / "AGENT.md"
    if agent_path.exists():
        agent_content = agent_path.read_text(encoding="utf-8")
        if "MEMORY.md" not in agent_content:
            # Insert after SYSTEM.md in the reading order
            agent_content = agent_content.replace(
                "| 3 | **RUNBOOK.md**",
                "| 3 | **MEMORY.md** | Your experience from building this before — read this |\n"
                "| 4 | **RUNBOOK.md**"
            )
            agent_content = agent_content.replace(
                "| 4 | **modules/",
                "| 5 | **modules/"
            )
            agent_path.write_text(agent_content, encoding="utf-8")

    return files


# =============================================================================
# STANDALONE CLI
# =============================================================================

if __name__ == "__main__":
    print("\nImperfektum Engine v1.0")
    print("Generates agent memory from a Project Forge blueprint.\n")
    print("Usage:")
    print("  As library:  from imperfektum_engine import ImperfektumEngine")
    print("  With Forge:  from imperfektum_engine import forge_with_memory")
    print("\nSee docstrings for integration details.")
