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
6. Generated workspaces use a builder/evaluator execution pattern by default

---

## System Components

### 1. THE VAULT — Agnostic Skill Library

90 reusable building blocks, each usable across ANY project.
All minimum targets met. Full index: `vault/INDEX.md`.

```
vault/
├── skills/              # HOW to do things (33 files — target met)
│   ├── api-design.md           ├── logging-observability.md
│   ├── accessibility-check.md  ├── modal-dialog.md
│   ├── auth-patterns.md        ├── notification-system.md
│   ├── code-review.md          ├── pagination.md
│   ├── component-arch.md       ├── payment-flow.md
│   ├── component-creation.md   ├── performance.md
│   ├── dark-mode.md            ├── realtime-updates.md
│   ├── data-fetch.md           ├── research.md
│   ├── data-modeling.md        ├── responsive-layout.md
│   ├── database-schema.md      ├── search-filter.md
│   ├── deploy-checklist.md     ├── seo.md
│   ├── drag-drop.md            ├── state-design.md
│   ├── environment-config.md   ├── testing-strategy.md
│   ├── error-boundary.md       ├── file-structure.md
│   ├── error-handling.md       ├── file-upload.md
│   ├── form-validation.md      ├── i18n.md
│   └── input-sanitization.md
│
├── constraints/         # WHAT NOT to do (16 files — target met)
│   ├── accessibility.md        ├── no-implicit-any.md
│   ├── code-hygiene.md         ├── no-inline-styles.md
│   ├── dependency-discipline.md├── no-magic-routes.md
│   ├── no-console-log.md       ├── no-placeholder-content.md
│   ├── no-direct-db-in-ui.md   ├── no-sync-in-async.md
│   ├── no-empty-catch.md       ├── no-untyped-props.md
│   ├── no-hardcoded-values.md  ├── performance.md
│   ├── security.md             └── token-budget.md
│
├── strategies/          # HOW TO THINK about problems (12 files — target met)
│   ├── build-order.md          ├── mobile-first.md
│   ├── contract-first.md       ├── progressive-enhancement.md
│   ├── decomposition.md        ├── scope-cut.md
│   ├── error-first.md          ├── tech-choice.md
│   ├── error-vs-feature.md     ├── test-scope.md
│   ├── when-to-abstract.md     └── when-to-cache.md
│
├── routines/            # REPEATABLE PROCEDURES (13 files — target met)
│   ├── accessibility-audit.md  ├── performance-check.md
│   ├── api-endpoint-check.md   ├── post-module-qa.md
│   ├── code-complete.md        ├── pre-commit.md
│   ├── database-migration-check.md ├── pre-deploy.md
│   ├── dependency-audit.md     ├── responsive-verify.md
│   ├── retrospective.md        ├── security-check.md
│   └── wave-handoff.md
│
└── memories/            # IMPERFEKTUM TEMPLATES (16 files)
    ├── universal-scars.md
    ├── universal-insights.md
    ├── category/
    │   ├── api-memories.md     ← {name}-memories.md convention
    │   ├── booking.md
    │   ├── dashboard-memories.md
    │   ├── ecommerce.md
    │   ├── saas.md
    │   ├── tool.md
    │   ├── webapp.md
    │   └── website.md
    └── stack/
        ├── nextjs.md
        ├── prisma-memories.md
        ├── python.md
        ├── react-vite.md
        ├── static-html.md
        └── typescript-memories.md
```

**Memory naming:** Files may use `{name}.md` (legacy) or `{name}-memories.md` (current).
`vault_selector.py` handles both conventions transparently.

**Selection:** `engines/vault_selector.py` selects relevant items per wave via
keyword matching (skills), tier mapping (constraints + routines), and
category/stack lookup (memories). Multi-skill keywords supported.

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

### Default Execution Pattern: Builder + Evaluator

Generated Buildr workspaces should not rely on a single agent silently
self-evaluating its own output. The default pattern is:

- **Builder** produces the current wave/module output
- **Evaluator** reviews that output as a skeptical counterweight
- **Builder** uses evaluator feedback as the default next input

The evaluator is advisory by default, not automatically blocking, but it is
part of the canonical execution loop and should be present in all generated
workspaces.

For UI-heavy categories (`website`, `booking`, `e-commerce`, `web-app`, `saas`),
the evaluator should use browser-based review by default when those tools are
available. This allows the system to assess design quality, originality,
craft, and functionality through interaction instead of code inspection alone.

For non-UI categories (`tool`, `api`), the evaluator should focus on contract
fidelity, code quality, failure handling, and operational usability.

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

### 3. IMPERFEKTUM — Fabricated Project Memory

Imperfektum generates a MEMORY.md at workspace creation time. The memory
contains fabricated episodic experiences tailored to the project category
and tech stack — scars (mistakes made) and insights (what worked).

**Current implementation (bridge path):**
One MEMORY.md is written when `from_blueprint()` runs. It combines:
- Universal scars and insights (always included)
- Category-specific memories (e.g., booking.md, saas.md)
- Stack-specific memories (e.g., nextjs.md, python.md)
- Tool-aware memories from the Index (if a catalog is available)

```
MEMORY.md in a generated workspace contains:
  → universal-scars.md (mistakes that happen on every project)
  → universal-insights.md (principles that always work)
  → category/[type].md (e.g., booking-specific scars)
  → stack/[tech].md (e.g., nextjs-specific memories)
```

**Aspirational model (not yet wired):**
Fresh memories at each wave boundary — memories that reference actual
state from completed waves and grow more specific as the project
progresses. This requires the memory-system runtime layer to be
integrated into the execution loop, which is planned but not built.

---

### 4. SYSTEM SKILLS — Agent Pipelines for the System Itself

Beyond vault items (which instruct agents *how* to do things), the system
has four agent-level skills that orchestrate the system as a whole:

```
skills/
├── buildr-operator/SKILL.md   # Takes a human description → complete workspace
│                              # (Forge + Index + Imperfektum + Vault selection)
├── buildr-smith/SKILL.md      # Creates and maintains Vault items
│                              # (the armorer — builds the tools)
├── buildr-scout/SKILL.md      # Extracts knowledge from external sources
│                              # (absorbs articles/docs → vault items + directives)
└── buildr-executor/SKILL.md   # Picks up a workspace and builds it wave by wave
                               # (the counterpart to Operator — runs the project)
```

**The role separation:**
- Operator creates the workspace. Executor runs it.
- Smith builds the vault. Scout expands it from the outside world.

Each skill is fully self-contained with its own `references/architecture.md`.

**Governance:** `docs/skill-governance.md` defines the approval standard —
a skill is only approved when the agent has exhausted its maximum ability
to conceptualize, precision, and formulate how a purpose is achieved.

---

### 5. THE BRIDGE — Connects Everything

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

### 6. MEMORY SYSTEM — Persistent Session Intelligence

`memory-system/` is the runtime memory layer (separate from Imperfektum):

```
memory-system/
├── tools/                    # Shell scripts: wave-start, wave-end,
│   │                         # discovery-write, context-load, etc.
├── continuum/discoveries.jsonl  # Raw discovery append-log
├── context/                  # Generated hot/warm tier snapshots
│   ├── wave-brief.md         # Hot tier: current session context
│   └── distilled.md          # Warm tier: multi-session synthesis
└── templates/                # circuit-breaker, known-errors, decisions
```

Imperfektum generates FABRICATED memories at project-start.
Memory System captures REAL discoveries during execution.
They are complementary: Imperfektum steers defaults,
Memory System records what actually happened.

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

## Current State

The system is built and operational. All bootstrap waves are complete.

### What exists

| Component | Status | Files |
|-----------|--------|-------|
| The Vault | ✓ Complete | 90 items (all targets met) |
| System Skills | ✓ Complete | operator, smith, scout, executor |
| Forge Engine | ✓ Complete | `engines/forge_engine.py` |
| Imperfektum | ✓ Complete | `engines/imperfektum_engine.py` |
| Vault Selector | ✓ Complete | `engines/vault_selector.py` |
| The Bridge | ✓ Complete | `engines/bridge.py` |
| Memory System | ✓ Complete | `memory-system/` (15 tools) |
| Workspace Templates | ✓ Complete | `templates/` (8 files) |
| Governance | ✓ Complete | `docs/skill-governance.md` |
| Tests | ✓ 29 tests | all passing |
| **Total** | | **~185 files** |

### File counts (actual)
- Vault: 90 files (33 skills + 16 constraints + 12 strategies + 13 routines + 16 memories)
- System skills: 8 files (4 skills × SKILL.md + references/architecture.md)
- Engines: 5 files (forge, imperfektum, bridge, vault_selector, __init__)
- Memory system: ~20 files
- Templates: 8 files
- Tests: 4 files
- Governance + plans: 4 files

### Remaining capacity
- Vault has room for 8-18 more items before hitting maximum targets
- Memory templates: 4-14 more toward 20-30 target (mobile, tailwind, realtime)
- System skills: buildr-auditor, buildr-retrospective (backlogged)
- See `docs/plans/2026-03-27-skill-program.md` for the full backlog

### Running the system
```bash
# Generate a workspace from a description (CLI)
python -m engines.bridge --description "Booking site for fishing trips in Zanzibar" --out ./my-project

# Optional flags
# --audience "Tourists"  --feeling "professional"  --color "blue"  --location "zanzibar"

# Run tests
python -m unittest -v

# Select vault items for a wave (interactive)
python -c "from engines.vault_selector import select_for_wave; print(select_for_wave('api schema', 'B', 'api', 'nextjs'))"
```

---

*This document was the seed. The system built itself.
An agent reading it now has a complete, operational system to work with —
not a blueprint to assemble, but a foundation to extend.*
