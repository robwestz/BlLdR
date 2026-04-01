# Phase Depth Reference — Buildr Workspace Architect

> **Canonical rule:** `SKILL.md` is the authoritative execution procedure. This file adds reasoning depth, anti-patterns, and drift prevention. Large procedural duplication between this file and `SKILL.md` is forbidden. If you need the step-by-step procedure, read `SKILL.md`. If you need to understand why a phase works the way it does, read this file.

---

## Phase 1: Purpose Extraction — Reasoning Depth

### The Core Problem Phase 1 Solves

Most project failures trace back to a misunderstood purpose — not a wrong technology, not a bad developer, but a project that was built to solve Problem A when the user meant Problem B. Phase 1 exists to freeze the purpose before any technical reasoning begins.

### Why CRI Is Extracted Here (Not Later)

Commercial Reality Invariants must be extracted before architecture, because architecture serves commerce — not the reverse. If the monetization model is `subscription` but the architecture assumes `transaction_fee`, the minimal-inevitable set will be wrong. CRI is non-negotiable input to Phase 3, not a decorative addition to Phase 1.

### Anti-Collapse Rules for Phase 1

- **Do not merge purpose extraction with architecture.** Phase 1 asks "what are we solving?" Phase 3 asks "what is the minimum structure to solve it?" Merging them causes premature technical commitment.
- **Do not skip CRI for "internal tools."** Even internal tools have a target user class, a job-to-be-done, and a business outcome. `monetization_model: none` is a valid CRI value. Leaving it blank is not.
- **Do not list features as purpose claims.** "The system has a login page" is a feature. "Users can securely access their personal data" is a purpose claim. Purpose claims are testable against user outcomes, not system inventory.

### Phase 1 Anti-Patterns

| Anti-Pattern | What It Looks Like | Why It Fails |
|-------------|-------------------|-------------|
| **Feature List Masquerading as Purpose** | "Purpose: login, dashboard, reports, settings" | No falsifiable claims. No user outcome. Architecture becomes feature checklist. |
| **Vague User Class** | "Target users: everyone" or "Target users: users" | Architecture cannot be scoped. Everything seems necessary. |
| **Skipped Kill-Switch** | `kill_switch_triggers: []` for a time-constrained project | No binary abort condition. Project drifts past deadline without a clear stop signal. |
| **Assumed Monetization** | For-profit intent with `monetization_model` left blank | Architecture may miss payment infrastructure, pricing page, trial mechanics. Late discovery is expensive. |

### What Phase 1 Must Never Do

- Never propose technical solutions. "We should use PostgreSQL" is a Phase 3/4 concern.
- Never resolve ambiguity through assumption when it can be asked. Assumptions are recorded, not hidden.
- Never filter the human description. Capture everything, then structure it. Missing nuance costs more than capturing irrelevance.
- Never produce CRI fields that disagree with the human description. If the description says "free tool," `monetization_model` is `none`, not `unknown`.

### Examples of Drift Between Phase 1 and Phase 3

- Phase 1 says "target users are tourists." Phase 3 designs a desktop-first admin dashboard. The drift: architecture forgot who it serves.
- Phase 1 says `monetization_model: subscription`. Phase 3 omits subscription management from the minimal set. The drift: CRI was recorded but not consumed.
- Phase 1 lists `kill_switch_triggers: ["if payments cannot be integrated within 2 weeks"]`. Phase 3 treats payment as a Phase 2 wave concern. The drift: the kill switch exists to prevent exactly this deferral.

---

## Phase 2: Absence Mapping — Reasoning Depth

### The Core Problem Phase 2 Solves

What you don't know is more dangerous than what you know wrong. A wrong assumption can be corrected. An unknown assumption cannot be corrected because nobody knows it exists. Phase 2 makes unknowns visible.

### Why ELS Is Mandatory (Not Optional)

The six ELS categories represent the classes of failure that destroy budgets: security breaches, compliance violations, accessibility lawsuits, payment processing errors, data governance fines, and legal exposure. These are not theoretical — they are the categories that turn a fixable bug into a project-ending event.

Forcing every project through all six categories ensures that "not applicable" is a conscious, justified decision rather than an oversight.

### Anti-Collapse Rules for Phase 2

- **Do not merge absence mapping with architecture.** Phase 2 asks "what don't we know?" Phase 3 asks "what must we build?" An absence is not a component. "We don't know the payment provider" (absence) is not the same as "we need a payment module" (component).
- **Do not collapse ELS into a single "risks" section.** Each of the six categories has different stakeholders, different consequences, and different mitigation timelines. Collapsing them hides category-specific risks behind generic language.
- **Do not mark ELS categories as `not_applicable` without proof.** The proof must be a one-line factual statement (e.g., "No user-facing UI exists, confirmed by CRI"). "Not relevant" without evidence is not a proof.

### Phase 2 Anti-Patterns

| Anti-Pattern | What It Looks Like | Why It Fails |
|-------------|-------------------|-------------|
| **Optimistic Absence** | "No significant gaps identified" for a two-sentence description | A two-sentence description has many gaps. The absence map failed to find them. |
| **Risk Theater** | Long list of generic risks ("data could be breached") with no project-specific analysis | Generic risks don't inform architecture. "AuthZ boundary between tenant A and tenant B's booking data" does. |
| **ELS Checkbox** | All six categories marked with one-line entries | ELS is not a compliance checkbox. Each category requires analysis proportional to its relevance. |
| **Deferred Everything** | Most absences classified as `deferrable` | If everything is deferrable, the analysis did not assess architectural impact. Deferral is appropriate only when the absence does not affect the minimal-inevitable set. |

### What Phase 2 Must Never Do

- Never propose solutions. "We should use OAuth" is Phase 3/4 territory. Phase 2 says "authentication model is unspecified."
- Never minimize a category's relevance without factual basis. "Security is probably fine" is not analysis.
- Never invent information to fill gaps. If the description does not mention payment, the absence is real. Do not infer payment details from thin signals.
- Never classify a `blocking` absence as `deferrable` to keep the pipeline moving. If it blocks architecture, it blocks.

### Examples of Hiding Uncertainty Inside Architecture Language

- "The auth module will handle authentication" — this hides the absence (which auth model? SSO? OAuth? Email/password? Magic links?) inside a confident-sounding architectural statement.
- "Data will be stored securely" — this hides the absence (which data? what security model? what compliance regime?) inside reassuring language.
- "The API will be scalable" — this hides the absence (what load? what SLO? what scaling model?) inside aspirational language.

Phase 2 must surface these as absences, not let them pass as architecture.

---

## Phase 3: Minimal-Inevitable Architecture — Reasoning Depth

### The Core Problem Phase 3 Solves

Most architecture is bloated because it is designed for imagined futures rather than stated purposes. Phase 3 forces the opposite: what is the absolute minimum that satisfies the stated purpose? Nothing more.

### The "Inevitable" Test

A component is inevitable when:
1. At least one purpose claim cannot be satisfied without it.
2. Removing it breaks a stated purpose (not an assumed nice-to-have).
3. No simpler alternative exists that satisfies the same purpose claim.

"Inevitable" is not "important" or "best practice" or "industry standard." Many important, best-practice, industry-standard components are not inevitable for a specific project's stated purpose.

### Anti-Collapse Rules for Phase 3

- **Do not merge architecture with implementation.** Phase 3 says "the system needs a persistent data store." It does not say "use PostgreSQL with Prisma." Technology choice is a Phase 4 decision or an operator-level derivation.
- **Do not merge acceptance criteria with architecture narrative.** Architecture explains what exists and why. Acceptance criteria define how to verify it works. These are structurally different concerns with different audiences (architecture for builders, acceptance for testers/reviewers).
- **Do not include "nice-to-haves" in the minimal set with a note that they are optional.** If it is optional, it is not minimal-inevitable. Put it in `non_goals` with a justification.

### Phase 3 Anti-Patterns

| Anti-Pattern | What It Looks Like | Why It Fails |
|-------------|-------------------|-------------|
| **Kitchen Sink Architecture** | 15+ components in the "minimal" set | If the purpose has 3 claims and the architecture has 15 components, most components are not purpose-driven. |
| **Premature Tech Choice** | "Minimal architecture: Next.js + Prisma + PostgreSQL + Tailwind + Redis" | These are implementation decisions, not architectural components. "Web application framework," "persistent data store," "styling system" are architectural. |
| **Subjective Acceptance** | "AC-001: The UI looks professional" | Not verifiable. What does "professional" mean? Replace with measurable proxy: "AC-001: Design system tokens are applied consistently; no raw hex values in components." |
| **Missing Purpose Mapping** | Acceptance criteria exist but don't reference purpose claims | Criteria without purpose mapping are untethered — they might test the wrong thing. |

### What Phase 3 Must Never Do

- Never include a component because "most projects need it." Only include it because THIS project's purpose claims require it.
- Never define implementation details. "REST API" is architectural. "Express.js with cors middleware" is implementation.
- Never write acceptance criteria that require human judgment. "Looks good" fails. "Returns HTTP 200 with JSON body matching schema" passes.
- Never accept fewer acceptance criteria than the minimum formula requires. If `purpose_claims * 2` demands 8 criteria and you only have 6, the phase fails. Write more specific criteria, do not reduce the bar.

### Examples of Overspecializing Too Early

- Phase 3 specifies "PostgreSQL" when the purpose only requires "persistent structured data." The technology choice should survive challenge in Phase 4, but it should not be baked into Phase 3's minimal set.
- Phase 3 specifies "WebSocket-based real-time updates" when the purpose only requires "users see changes without manual refresh." The mechanism is an implementation detail.
- Phase 3 specifies "microservices architecture" when the purpose has 3 claims and a single-user class. The deployment topology is not architecturally inevitable — it is a scaling decision.

---

## Phase 4: Skeptical Challenge — Reasoning Depth

### The Core Problem Phase 4 Solves

Confirmation bias. Phase 3 proposes an architecture and the natural tendency is to accept it because it was the work product. Phase 4 exists to force genuine adversarial examination of every commitment.

### Why One Pass, Not Iteration

The challenge loop uses one pass for three reasons:

1. **Minimal-inevitable architecture is resistant to challenge by design.** If the Phase 3 process correctly applied the "inevitable" test, most components will survive challenge. A second pass rarely finds what the first missed.
2. **Iteration introduces decision fatigue.** Each additional pass produces diminishing returns and increasing risk of arbitrary changes.
3. **Unresolved items have a proper destination.** Items that survive challenge are confirmed. Items that fail are adjusted or rejected. Items that are ambiguous become `known_unknowns` with `open_risks` entries. No item lacks a resolution path after one pass.

If the first challenge pass reveals that the architecture is fundamentally wrong (not adjustable, but wrong), the correct outcome is `rejected` — not more iteration on a broken foundation.

### Anti-Collapse Rules for Phase 4

- **Do not merge challenge with architecture revision.** Phase 4 challenges. If adjustments are needed, they are recorded as decisions with rationale, not silently applied to Phase 3 artifacts. Phase 3 artifacts are not rewritten — decisions record what changed and why.
- **Do not present strawman alternatives.** Each `alternatives_considered` entry must be a genuinely viable option that a competent architect might choose. "Do nothing" or "use a technology from 2005" are not genuine alternatives.
- **Do not confuse reversibility with importance.** A high-reversibility-cost decision is not necessarily a bad decision. It is a decision that requires explicit ownership because the cost of being wrong is high.

### Phase 4 Anti-Patterns

| Anti-Pattern | What It Looks Like | Why It Fails |
|-------------|-------------------|-------------|
| **Rubber Stamp Challenge** | "All components confirmed, no issues found" | Either the challenge was not genuine, or the architecture was not examined critically. Even a correct architecture has decisions with non-trivial alternatives. |
| **Challenge Creep** | Challenge invents new requirements not in the original description | Phase 4 challenges existing commitments against stated purpose. It does not expand scope. |
| **Strawman Alternatives** | "Alternative: use no database. Rejected: impossible." | This is not a genuine alternative. A genuine alternative: "Use SQLite instead of a managed database. Rejected: concurrent multi-user access pattern in purpose claim 2 requires connection pooling." |
| **Risk Minimization** | `reversibility_cost_if_wrong: low` for a database schema choice | Database schemas are high-cost to reverse (data migration, downtime, application rewrite). Understating reversibility cost is dangerous. |

### What Phase 4 Must Never Do

- Never add new components to the minimal set. Phase 4 removes or confirms — it does not expand.
- Never introduce new purpose claims. The purpose was frozen in Phase 1.
- Never resolve ambiguity by assuming. If a decision cannot be made with available information, it becomes a `known_unknown` with a mitigation plan.
- Never skip the decision record for a significant commitment. "Significant" means: the commitment constrains downstream implementation choices.

---

## Phase 5: Approval Synthesis — Reasoning Depth

### The Core Problem Phase 5 Solves

Phase 5 prevents the anti-pattern of "good analysis, no decision." All prior phases produce analysis. Phase 5 converts that analysis into a binary gate: the workspace may or may not be generated.

### Why Three Statuses, Not Two

`approved` and `rejected` are clear. `insufficient_information` exists because many real projects are neither approvable nor rejectable — they need more input. Forcing a binary approved/rejected would cause either:
- Premature approval (generating from incomplete information), or
- Premature rejection (killing a viable project because information is temporarily missing).

`insufficient_information` is not a soft rejection. It is a request for specific inputs that will unblock a subsequent preflight run.

### Anti-Collapse Rules for Phase 5

- **Do not merge approval with any prior phase.** Phase 5 is synthesis, not analysis. It reads outputs from all prior phases and makes a determination. It does not re-analyze.
- **Do not add new analysis in Phase 5.** If Phase 5 discovers something that Phases 1-4 missed, this indicates a gap in the earlier phases, not a Phase 5 responsibility. Record it, but do not expand Phase 5 into re-analysis.
- **Do not use `approved` as a synonym for "probably fine."** `approved` means: all binary gates pass, all CRI fields are populated, all ELS categories are addressed, all decisions are recorded, acceptance criteria meet the minimum, and a non-empty approval basis exists. If any of these are not true, the status is not `approved`.

### Phase 5 Anti-Patterns

| Anti-Pattern | What It Looks Like | Why It Fails |
|-------------|-------------------|-------------|
| **Approval Without Basis** | `status: approved, approval_basis: []` | An approval without stated evidence is not an approval. It is an abdication. |
| **Conditional Approval** | "Approved, pending resolution of XYZ" | There is no conditional approval. Either the condition is a `known_unknown` with a mitigation plan (approved with open risk), or it is a `required_missing_input` (insufficient_information). |
| **Soft Rejection** | `status: rejected` with vague reasons like "needs more thought" | Rejection reasons must be specific and tied to a failed binary gate. "Needs more thought" is not a gate failure. |
| **Scope Expansion in Synthesis** | Phase 5 adds new acceptance criteria or architectural components | Phase 5 synthesizes — it does not create. New concerns should have been caught in Phases 1-4. |

### What Phase 5 Must Never Do

- Never change the status to accommodate time pressure. The gates are binary. They pass or they do not.
- Never approve if `monetization_model: unknown` for a clearly for-profit project without explicit `non_goals` exclusion and user acknowledgment.
- Never approve if a `payments_and_money_movement` or `privacy_and_data_governance` ELS risk has `residual_open_risk: true` without user-explicit acceptance in decisions.
- Never produce a `PREFLIGHT_BUILD_ORDER.md` for a non-approved project.

---

## Cross-Phase Drift Prevention

### How Phases Can Drift

| Drift Type | Example | Prevention |
|-----------|---------|-----------|
| **Purpose drift** | Phase 3 architecture serves a different user than Phase 1 specified | Phase 3 must reference `target_customer_or_user_class` when justifying components |
| **CRI drift** | Phase 4 decisions ignore `monetization_model` | Decision records must include `selected_rationale` tied to `purpose_claims` |
| **Acceptance drift** | Phase 3 criteria don't map to Phase 1 claims | Every criterion requires `purpose_claim_refs[]` — unmapped criteria are rejected |
| **Scope drift** | Phase 4 adds components not justified by purpose claims | Phase 4 may only confirm, adjust, or remove — never add |
| **Gate erosion** | Phase 5 approves despite a failed Phase 3 minimum | Phase 5 must verify each prior gate explicitly, not by assumption |

### The Anti-Collapse Guarantee

The phases exist to force structured, sequential reasoning with explicit gates between stages. Collapsing them — even if the collapsed version covers the same topics — defeats the mechanism because:

1. **Without explicit gates, there is no point at which the pipeline can halt.** A collapsed analysis always reaches a conclusion. A gated pipeline can stop at Phase 2 if information is missing.
2. **Without separate artifacts, there is no reviewability.** A user can read `PREFLIGHT_PURPOSE.md` and decide if the purpose is correct before architecture begins. In a collapsed analysis, purpose and architecture are interleaved.
3. **Without inter-phase contracts, there is no drift detection.** Phase 3 must consume Phase 1 outputs. If they are not separate artifacts, there is nothing to consume — and nothing to catch when architecture drifts from purpose.
