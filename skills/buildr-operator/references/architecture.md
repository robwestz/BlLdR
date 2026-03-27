# BUILDR SYSTEM ARCHITECTURE
## Forge × Index × Imperfektum × Orchestration

> This document defines the complete system and serves as the bootstrap
> instruction for an agent to assemble it.

---

## The Core Insight

95% of what makes an agent effective is project-agnostic. Research skills,
validation routines, code review checklists, architecture patterns, testing
strategies, error recovery procedures — these are identical whether you're
building a booking site, a SaaS platform, or a CLI tool.

The remaining 5% is project-specific: the product vision, the domain model,
the target audience, the design language.

The system is designed so that:
1. The agnostic 95% lives in a reusable library (The Vault)
2. The specific 5% is generated per-project (Forge onboarding)
3. Work is sequenced in waves with progressive disclosure (Orchestration)
4. Fabricated episodic memory steers agent behavior (Imperfektum)
5. Everything is cataloged and retrievable (The Index)

---

## System Components

### 1. THE VAULT — Agnostic Skill Library

A collection of ~100 reusable building blocks, each usable across ANY project.
Every block follows the same format:

```
vault/
├── skills/              # HOW to do things
│   ├── research.md         # How to research a topic systematically
│   ├── code-review.md      # How to review code for quality
│   ├── api-design.md       # How to design a REST/GraphQL API
│   ├── component-arch.md   # How to architect UI components
│   ├── data-modeling.md    # How to design data models
│   ├── error-handling.md   # How to implement error handling
│   ├── testing-strategy.md # How to plan and write tests
│   ├── performance.md      # How to optimize for performance
│   ├── accessibility.md    # How to build accessible interfaces
│   ├── responsive.md       # How to build responsive layouts
│   ├── state-management.md # How to manage application state
│   ├── form-validation.md  # How to validate user input
│   ├── auth-patterns.md    # How to implement authentication
│   ├── payment-flow.md     # How to implement payment flows
│   ├── i18n.md             # How to internationalize
│   ├── seo.md              # How to optimize for search engines
│   ├── deploy.md           # How to deploy to production
│   └── ...                 # (target: 30-40 skills)
│
├── constraints/         # WHAT NOT to do
│   ├── code-hygiene.md     # No console.log, no inline styles, etc.
│   ├── token-budget.md     # Budget tracking rules
│   ├── file-discipline.md  # File naming, structure, limits
│   ├── dependency.md       # Minimize external deps, justify each
│   ├── security.md         # Input sanitization, no secrets in code
│   ├── accessibility.md    # WCAG AA minimum, semantic HTML
│   ├── performance.md      # Bundle size limits, image optimization
│   └── ...                 # (target: 15-20 constraints)
│
├── strategies/          # HOW TO THINK about problems
│   ├── decomposition.md    # Break large tasks into small steps
│   ├── progressive-enhancement.md  # Build simple first, layer complexity
│   ├── contract-first.md   # Define interfaces before implementation
│   ├── mobile-first.md     # Design for smallest viewport first
│   ├── error-first.md      # Handle errors before happy path
│   ├── 30-70-rule.md       # Implement 30% that's hardest to design
│   └── ...                 # (target: 10-15 strategies)
│
├── routines/            # REPEATABLE PROCEDURES (like QA)
│   ├── module-qa.md        # Post-module quality checklist
│   ├── pre-deploy.md       # Pre-deployment verification
│   ├── code-complete.md    # Definition of "done" for a code unit
│   ├── ux-review.md        # UX quality verification
│   ├── responsive-check.md # Responsive breakpoint verification
│   ├── retrospective.md    # Post-phase retrospective template
│   └── ...                 # (target: 10-15 routines)
│
├── contracts/           # INTERFACE TEMPLATES
│   ├── api-contract.md     # REST API contract template
│   ├── component-contract.md # UI component contract template
│   ├── data-contract.md    # Data model contract template
│   ├── integration-contract.md # Third-party integration template
│   └── ...                 # (target: 5-10 templates)
│
└── memories/            # IMPERFEKTUM TEMPLATES
    ├── universal-scars.md  # Mistakes that apply to ALL projects
    ├── universal-insights.md # Approaches that always work
    ├── category/
    │   ├── booking-scars.md
    │   ├── ecommerce-scars.md
    │   ├── webapp-scars.md
    │   ├── saas-scars.md
    │   └── ...
    └── stack/
        ├── nextjs-scars.md
        ├── react-vite-scars.md
        ├── python-scars.md
        └── ...
```

### KEY PROPERTY: Every file in The Vault is COMPLETE and SELF-CONTAINED.
An agent can read any single file and use it immediately without needing
any other file. No file references another file in The Vault.

### KEY PROPERTY: Every file is AGNOSTIC.
It says "when building a form, always validate on blur AND on submit"
— not "for the Zanzibar booking site, validate the email field."
The project-specific 5% is injected at runtime by the orchestrator.

---

### 2. THE ORCHESTRATOR — Wave-Based Execution

Based on the orchestration kit pattern. The orchestrator:

1. Reads project state (what's done, what's next)
2. Plans the CURRENT wave only (not future waves)
3. Selects relevant Vault items for this wave
4. Generates phase-specific Imperfektum memories
5. Executes the wave
6. Updates state
7. Repeats

**Why this solves the N² context problem:**

Traditional approach: Plan all N modules, maintain N×(N-1)/2 context links.
Wave approach: Plan only the current wave. State captures decisions.
Contracts capture interfaces. Completed waves are never re-read.

At wave 9, the agent doesn't need to "remember" waves 1-8.
It needs only: state file + active contracts + current wave spec.

```
state/orchestration.yaml    ← "Where am I? What's decided? What's the budget?"
contracts/                  ← "What are the interfaces between completed and future work?"
waves/current-wave.md       ← "What am I doing RIGHT NOW?"
vault/[selected items]      ← "What skills/constraints apply to THIS wave?"
```

**The organic planning principle:**

Wave 1 is planned during onboarding.
Wave 2 is planned AFTER wave 1 completes — using the actual results, not predictions.
Wave 3 is planned after wave 2.

Each wave's plan is sharper than any upfront plan could be, because it's informed
by what actually happened in previous waves.

---

### 3. IMPERFEKTUM — Phase-Specific Memory Generation

Instead of generating one big MEMORY.md at project start, Imperfektum generates
FRESH memories at each wave boundary:

```
Before Wave 1 (Foundation):
  → Universal scars + foundation-specific insights
  → Memory of what "done" looks like for this wave specifically

Before Wave 2 (Design System):
  → Universal scars + design-system scars
  → "Last time we built the design system, we made 5 base components and
     tested each one at 3 breakpoints before moving on. That discipline
     saved us 2 days of rework later."

Before Wave 3 (Core Feature):
  → Category-specific scars (booking calendar, e-commerce cart, etc.)
  → Memories informed by what Wave 1 and 2 ACTUALLY produced
  → "The design system we built in Wave 2 uses CSS variables for all colors.
     When building the calendar component, we MUST use these variables."
```

This means the memories get MORE SPECIFIC as the project progresses,
because each wave's memory can reference actual state from completed waves.

---

### 4. THE BRIDGE — Connects Everything

```python
class SystemOrchestrator:
    """The runtime that ties Vault + Orchestration + Imperfektum + Index together."""

    def execute_wave(self, wave_number: int):
        # 1. Read state
        state = self.read_state()

        # 2. Read current wave spec
        wave = self.read_wave(wave_number)

        # 3. Select relevant Vault items for this wave
        skills = self.vault.select_skills(wave.intent, wave.tier)
        constraints = self.vault.select_constraints(wave.tier)
        routines = self.vault.select_routines(wave.tier)

        # 4. Generate phase-specific Imperfektum memory
        memory = self.imperfektum.generate_for_wave(
            wave=wave,
            state=state,
            completed_contracts=self.read_contracts(),
        )

        # 5. Assemble agent context for this wave
        context = self.assemble_context(
            state=state,
            wave=wave,
            skills=skills,
            constraints=constraints,
            memory=memory,
        )

        # 6. Execute (hand off to agent)
        result = self.agent.execute(context)

        # 7. Update state
        self.update_state(wave_number, result)

        # 8. Plan next wave (ORGANIC — based on actual results)
        if wave.is_last_planned:
            self.plan_next_wave(state, result)
```

---

## The Bootstrap Problem — And Its Solution

**Problem:** This system needs to be built. But it IS a system for building things.
Can it build itself?

**Yes.** Here's how:

### Bootstrap Wave 0: The Vault Foundation

An agent reads THIS DOCUMENT and creates the initial Vault structure.
It writes the first 10-15 skills, 5-7 constraints, 3-5 strategies, and 3-5 routines.
These are AGNOSTIC — they apply to building the system itself.

**Imperfektum memory for Wave 0:**
"Last time we built a reusable skill library, we made the mistake of writing
skills that were too abstract. The skills that worked best were ones that
contained specific, actionable instructions — 'validate on blur AND on submit'
not 'implement appropriate validation.' Every skill should read like a
checklist, not an essay."

### Bootstrap Wave 1: The Orchestration Engine

Using Wave 0's Vault, build the orchestration engine:
- state/orchestration.yaml schema
- Wave reader/executor
- State updater
- Vault selector (picks relevant items per wave)

### Bootstrap Wave 2: Imperfektum Integration

Using Waves 0-1, integrate Imperfektum:
- Phase-specific memory generator
- Wave-boundary memory injection
- Memory templates in Vault

### Bootstrap Wave 3: Forge Integration

Using Waves 0-2, integrate Project Forge:
- Onboarding → blueprint → wave plan
- Category-specific Vault item selection
- Design system derivation

### Bootstrap Wave 4: Index Integration

Using Waves 0-3, integrate The Index:
- Catalog the Vault
- Tool selection per wave
- Pack builder for distribution

### Bootstrap Wave 5: The Platform

Using everything above, build the deployable system:
- CLI entry point
- Web interface (optional)
- Distribution format

---

## The Manufactured Déjà Vu Effect

The deepest insight in this architecture:

The Vault's 100 agnostic items are REAL. They exist. They are reused
identically across projects. They are the genuine constants.

The Imperfektum memories are FABRICATED. They never happened. They are
manufactured experiences tailored to each specific context.

But from the agent's perspective, the relationship inverts:

- The Vault items feel NOVEL each time, because the 5% project-specific
  context modifies how they're applied. "validate on blur" means something
  different for a booking calendar vs. a CRM form.

- The Imperfektum memories feel REAL, because they carry narrative weight,
  specific details, and emotional consequence. The agent "remembers" the
  mistake and avoids it.

This inversion is the mechanism. The fake memories provide stability.
The real skills provide novelty. Together they create an agent that
behaves as if it has extensive, relevant experience with the specific
project it's building — even though it's its first time.

---

## Practical Next Steps

### To build the minimum viable system:

1. **Create The Vault** — 30 agnostic skills, 10 constraints, 5 strategies,
   5 routines. Each is a standalone .md file.

2. **Adapt the orchestration kit** — Use the uploaded SKILL.md pattern.
   Create: CLAUDE.md, RUN.md, state schema, wave template.

3. **Connect Imperfektum** — Generate phase-specific memories at wave
   boundaries using Vault memories as templates + state as context.

4. **Connect Forge** — Use onboarding to generate the project-specific 5%
   (description, audience, feeling, design system).

5. **Connect Index** — Catalog the Vault, enable tool/skill selection.

### File count for MVP:
- Vault: ~50 files (skills + constraints + strategies + routines)
- Orchestration: 5 files (CLAUDE.md, RUN.md, state, onboarding, wave template)
- Engines: 4 files (forge_engine.py, imperfektum_engine.py, bridge.py, vault_selector.py)
- Total: ~60 files, most of them small .md documents

This is not a large system. It's a small system with large leverage.

---

*This document is the seed. An agent reading it has everything needed
to begin the bootstrap. The system builds itself.*
