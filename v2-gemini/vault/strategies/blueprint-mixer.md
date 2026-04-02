# Blueprint Mixer Strategy (Gemini-v2 Multi-Composition)

## Purpose

To enable massive variation and ultra-high value project generation by allowing agents to compose a project's architecture from multiple independent Blueprints. This moves the system from "monolithic templates" to "modular DNA strings."

## Context

When a project description covers multiple domains (e.g., "A luxury booking site with an AI memory dashboard"), a single Blueprint is insufficient. The agent must be able to "mix" Blueprints without creating architectural conflicts.

## The Mixing Protocol

### 1. Identify the 'Anchor' Blueprint
Determine which Blueprint represents the primary business model (e.g., `booking` or `saas`). This Blueprint provides the `foundation` and `project-category` defaults.

### 2. Extract 'Traits' from Supplemental Blueprints
Identify supplemental Blueprints for specialized needs:
- **Design Trait:** (e.g., from `ultima-claw-ui-prime`) overrides the Anchor's design system, colors, and typography.
- **Logic Trait:** (e.g., from `zanzibar-premium-booking`) provides specific booking flows and data models.
- **Cognitive Trait:** (e.g., from `ultima-claw-ui-prime`) adds memory, identity, and budget monitoring modules.

### 3. Resolve Module Overlaps
When multiple Blueprints provide a module (e.g., both have `auth`), use the one from the most complex Blueprint (highest priority) or the one that matches the Tech Stack best.

### 4. Synthesize forced_constraints
Merge constraints. If conflicts occur:
- **Design constraints** from the UI-focused Blueprint take precedence.
- **Logic constraints** from the Domain-focused Blueprint take precedence.
- **Commercial (CRI) constraints** must be synthesized into a unified Business Outcome.

## Agent Mandate

An agent using the `buildr-advanced-operator` (Gemini Edition) MUST explicitly state when a project is a "Mixed Composition" and list the source Blueprints used.

**Example Response:**
"I have composed this project using the **Anchor: SaaS-Starter** for logic and **Supplemental: Ultima-Claw-UI-Prime** for design and cognitive memory features. The resulting architecture is a high-value Hybrid platform (400k+ SEK market value)."

## Verification

Before final approval, the agent must check:
- [ ] No duplicated modules with different interfaces.
- [ ] AC-IDs from ALL source Blueprints are represented in the final acceptance criteria.
- [ ] Design tokens (colors/fonts) are unified across all generated modules.

---

**AUTHOR_GATE: PASS**
