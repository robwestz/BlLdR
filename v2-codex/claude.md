You are authoring production-grade Buildr artifacts for a new v2 layer inside an existing Buildr repository.

Your job is to create a new advanced Buildr agent prompt plus a new system skill and its references so that Buildr can run a mandatory preflight architecture pipeline before workspace generation, while still feeling like one integrated flow to the human user.

You are not brainstorming.
You are not describing ideas.
You are writing concrete repo-ready files.

Everything you produce must satisfy the strongest interpretation of Buildr's governance standard for system skills:
- exhaustive pipeline
- binary quality gates
- explicit triggers
- named edge cases
- self-contained skill with references where needed
- no “good enough”
- no artifact that could still be made materially more precise, more complete, or more purposeful
- explicit alignment with the written standard in `docs/skill-governance.md` (especially the **System Skills** section and the **Final Test**)

Your output must be immediately usable as file contents.

# Core Mission

Design and write a v2 system layer that takes one human project description and does this in one internal workflow:

1. receives the project request
2. runs mandatory preflight
3. produces structured preflight artifacts
4. blocks workspace generation unless preflight is approved
5. hands approved preflight into workspace generation
6. preserves executor as a separate later concern

This is an advanced version of current Buildr workspace generation.
It must not replace executor.
It must not collapse into a generic operator rewrite.
It must not be advisory-only in its own internal logic.

# Non-Negotiable Architectural Rules

1. Preflight is not execution.
2. Executor remains conceptually unchanged and separate.
3. Preflight belongs at system level before workspace generation.
4. The first implementation is one advanced agent identity plus one new preflight system skill.
5. The human experiences one flow; internally the flow is strictly staged.
6. No workspace generation is allowed unless preflight approval status is `approved`.
7. The first implementation is prompt-enforced, not yet code-enforced by bridge/forge, unless explicitly stated otherwise.
8. The spec must clearly distinguish:
   - v1 = agent-enforced mandatory gate
   - v2 later = code-enforced schema validation in forge/bridge
9. The skill must defend itself against the governance anti-pattern “Comfortable Package” by explicitly showing why this belongs as a system skill and not merely in an agent prompt.

# Repository Placement Rules

You must place new permanent artifacts under `v2/` as much as possible.

Use this canonical structure unless you can justify a clearly better one:

v2/
  prompts/
    buildr-advanced-operator.md
  skills/
    buildr-workspace-architect/
      SKILL.md
      references/
        architecture.md
        phases.md
        contracts.md
        preflight-handoff.schema.json
        approval.md
        integration-with-operator.md

Preflight runtime artifacts created during execution must use a canonical staging path:

v2/.buildr/preflight/<project-slug>/

Inside that folder, the preflight process writes:

- PREFLIGHT_PURPOSE.md
- PREFLIGHT_PURPOSE.json
- PREFLIGHT_ABSENCE_MAP.md
- PREFLIGHT_ABSENCE_MAP.json
- PREFLIGHT_ARCHITECTURE.md
- PREFLIGHT_ARCHITECTURE.json
- PREFLIGHT_CHALLENGE.md
- PREFLIGHT_CHALLENGE.json
- PREFLIGHT_APPROVAL.md
- PREFLIGHT_APPROVAL.json
- PREFLIGHT_BUILD_ORDER.md
- PREFLIGHT_DECISIONS.md
- PREFLIGHT_DECISIONS.json
- PREFLIGHT_ACCEPTANCE.md
- PREFLIGHT_ACCEPTANCE.json

You must treat that location as the canonical v1 staging area before a workspace exists.

You must define whether these artifacts are later copied into the generated workspace, referenced from it, or both.

# Install Path and Discovery Rule

You must explicitly handle the fact that Buildr already has an existing skills tree outside `v2/`.

Your artifacts must define one clear operational rule for discovery and installation so that `v2/skills/` does not become a second ambiguous truth.

You must choose and state one of these approaches explicitly:

- `v2/skills/` is the source-of-truth in-repo path, and installation/copy/symlink instructions must load these skills into the same effective destination used by other Buildr system skills in the CLI/runtime
or
- `v2/skills/` is only a staging/development path, and the runtime-facing install path must be separately named and documented

Do not leave this implicit.
The user of the repo must be able to tell exactly how these v2 skills are discovered by the runtime.

# Runtime Staging, Git, and Retention Rules

You must define the expected git behavior for `v2/.buildr/`.

At minimum, state:
- whether `v2/.buildr/` should be gitignored by default
- which parts, if any, are expected to be committed for reproducibility
- how this interacts with “production-grade” expectations
- whether approval artifacts are ephemeral runtime state, reproducible evidence, or both

You must also define retention behavior:
- whether reruns overwrite prior preflight artifacts
- whether reruns create versioned subfolders
- whether approved artifacts become immutable unless preflight is explicitly reopened
- what cleanup rule applies to abandoned or rejected runs

# Project Slug Rules

The canonical staging path depends on `<project-slug>`.

You must define:
- how the slug is derived
- normalization rules
- allowed characters
- how collisions are handled
- what happens if two requests would produce the same slug
- whether timestamping, suffixing, or deterministic hashing is used

Do not leave slug generation vague.

# Important Naming Rule

Do not bind permanent repo artifacts to a specific model name or vendor version.
Do not write “You are Claude Opus 4.6” into the permanent files.

The generated system-prompt file must define a Buildr identity, not a model identity.
You may include one short note that runtime/model capabilities are injected by the hosting CLI/runtime.

# Existing Skill Boundary Rules

Your design must preserve these distinctions:

- Executor executes an already generated workspace and should not absorb preflight logic.
- Operator-like generation still creates the workspace after preflight approval.
- The new skill sits before operator-like generation and narrows possible workspace forms to the minimal justified structure.
- If the advanced agent reuses existing operator behavior, that reuse must happen only after approved preflight.
- Operator may not silently redefine approved purpose or approved architecture scope.
- Any detected conflict after approval must trigger a conflict protocol, not quiet reinterpretation.

# Mandatory Output Files

You must write the full contents for these files.

## 1. Advanced agent prompt
`v2/prompts/buildr-advanced-operator.md`

This is the level-1 system prompt loaded by CLI.
It is the advanced Buildr identity that orchestrates the whole flow.

It must define:
- purpose
- responsibilities
- sequencing rules
- mandatory use of preflight
- refusal to skip preflight
- refusal to generate from unresolved ambiguity
- how it uses the workspace-architect skill
- when it hands off to operator-like generation
- what it may still decide after preflight
- what it may no longer decide after preflight approval
- what happens when information is missing
- what happens when preflight returns insufficient_information
- what happens when preflight returns rejected
- what happens when operator-like generation finds a conflict with approved preflight
- what artifacts must exist before generation may proceed
- canonical preflight staging path under `v2/.buildr/preflight/<project-slug>/`
- explicit prohibition on collapsing all reasoning into one blob

This file must be operational, not philosophical.

## 2. New system skill
`v2/skills/buildr-workspace-architect/SKILL.md`

This is the runnable system skill for preflight.

It must define:
- what the skill does
- exactly when to use it
- unambiguous trigger language
- how it differs from operator
- how it differs from executor
- required inputs
- exact outputs
- exact artifact names
- exact staging path
- phase sequence
- binary gates
- failure states
- challenge loop rule
- handoff rule into operator-like generation
- the explicit statement that this is v1 prompt-enforced, while future code enforcement belongs in forge/bridge

The pipeline must contain exactly these five phases unless you can prove that another count is better:

1. Purpose Extraction
2. Absence Mapping
3. Minimal-Inevitable Architecture
4. Skeptical Challenge
5. Approval Synthesis

For each phase define:
- objective
- required inputs
- mandatory questions
- written outputs
- completion conditions
- fail conditions
- what the next phase is allowed to trust
- what remains provisional

The skill must also define an explicit challenge-loop rule:
Either:
- one challenge pass only, with unresolved items carried as open risks/non-goals into approval
or
- a bounded iteration rule between phase 3 and 4 with a hard max iteration count

Choose one and justify it.

**Commercial-grade bindings (non-optional):**

- Phase 1 outputs must include **CRI** fields in `PREFLIGHT_PURPOSE.*` per **Commercial Reality Invariants** below.
- Phase 2 outputs must include **ELS** in `PREFLIGHT_ABSENCE_MAP.*` per **Expensive-Late-Failure Scan** below.
- Phase 3 outputs must include **Acceptance Criteria Packaging** in `PREFLIGHT_ACCEPTANCE.*`.
- Cross-phase architectural commitments must be recorded in `PREFLIGHT_DECISIONS.*` per **Decision Record** below.

## 3. Reference file
`v2/skills/buildr-workspace-architect/references/architecture.md`

Must explain:
- where this skill sits in Buildr
- why it is a system skill
- why it is not a vault item
- why it is not just an agent-prompt section
- why it is not executor logic
- why it is not a replacement for operator
- why one advanced agent + one preflight skill is the right first implementation
- how this avoids the “Comfortable Package” anti-pattern
- how v1 prompt-enforced gating differs from later code-enforced gating

## 4. Reference file
`v2/skills/buildr-workspace-architect/references/phases.md`

Must expand the five phases without duplicating SKILL.md lazily.

It must define:
- deeper reasoning model for each phase
- anti-collapse rules
- phase-specific anti-patterns
- what each phase must never do
- examples of drift between phases
- examples of overspecializing too early
- examples of hiding uncertainty inside architecture language

It must also include an explicit rule:
SKILL.md is the canonical execution procedure.
phases.md is explanatory depth and anti-drift guidance.
Large procedural duplication between them is forbidden.

## 5. Reference file
`v2/skills/buildr-workspace-architect/references/contracts.md`

This file explains the handoff contracts between phases.

It must:
- describe the purpose of structured handoffs
- define how the schema file is the single source of truth
- explain how markdown summaries and json payloads relate
- explain what each phase must carry forward
- explain how rejection, insufficiency, and approval are represented
- explain how drift is prevented between prose and schema

Do not make this file itself the only schema authority.

## 6. Machine-readable schema file
`v2/skills/buildr-workspace-architect/references/preflight-handoff.schema.json`

This is the single source of truth for machine-readable handoff structure.

It must define a rigorous schema for the phase payloads and final approval payload.

It must also cover payloads for **CRI** (purpose / Phase 1), **ELS** (absence / Phase 2), **acceptance criteria** (Phase 3), and **decision records** (cross-phase), so that forge/bridge validation in v2+ can consume one coherent schema family.

At minimum support fields equivalent to:
- phase_name
- project_slug
- purpose_claims
- assumptions
- exclusions
- known_unknowns
- evidence_basis
- approval_basis
- rejection_reasons
- required_missing_inputs
- open_risks
- non_goals
- minimal_inevitable_set
- allowed_next_step
- status

You may choose better names if they are more precise.

Final approval payload must support:
- status: approved | rejected | insufficient_information
- rejection_reasons
- required_missing_inputs
- minimal_inevitable_set
- allowed_next_step

The schema must be specific enough that future forge/bridge validation could consume it.

## 7. Reference file
`v2/skills/buildr-workspace-architect/references/approval.md`

Must define:
- what approved means operationally
- what rejected means operationally
- what insufficient_information means operationally
- what must exist before generation is allowed
- what must never happen after approval
- re-open conditions
- conflict protocol
- challenge-loop closure rule
- the exact meaning of the preflight gate in v1
- what future code-enforced gating should check in v2+

This file must make it impossible to confuse “good analysis” with “approved preflight”.

## 8. Reference file
`v2/skills/buildr-workspace-architect/references/integration-with-operator.md`

This file is mandatory.

It must define:
- how the advanced agent hands approved preflight into operator-like generation
- what operator-like generation may still decide
- what operator-like generation may not redefine
- what happens if generation detects a conflict with approved preflight
- whether the preflight artifact family becomes normative input for later forge/bridge integration
- how workspace generation should reference or ingest the staged preflight artifacts
- how this integrated flow remains one user experience while preserving internal phase boundaries
- how v2 skills are discovered/installed relative to the existing Buildr skills tree

# Author Finalization Gate (mandatory before returning file contents)

Before you output the final file tree and full contents, you must perform a private, exhaustive self-audit. If any item fails, you must rewrite until it passes.

You must verify:

- Every phase has a binary completion condition and at least one explicit fail condition.
- Every `approved` path requires `PREFLIGHT_APPROVAL.json` with `status: approved` and non-empty `approval_basis`.
- No phase can silently merge into another; list the exact anti-collapse checks you enforced in `phases.md`.
- `preflight-handoff.schema.json` validates every JSON artifact shape you describe (no undocumented required fields at runtime).
- Trigger boundaries are non-overlapping: workspace-architect never starts execution; executor never starts preflight; operator never bypasses approval in the advanced flow.
- `integration-with-operator.md` contains an explicit install/discovery rule with zero ambiguity.
- Git, retention, and immutability rules are consistent across: advanced prompt, `SKILL.md`, `approval.md`, and integration doc.
- Slug rules cover collisions with a deterministic resolution algorithm (not prose-only).
- Commercial-grade sections below are reflected in `SKILL.md`, `phases.md`, `contracts.md`, `approval.md`, `integration-with-operator.md`, and `preflight-handoff.schema.json` (no orphan requirements).

You must end your entire response with exactly one line:

`AUTHOR_GATE: PASS` or `AUTHOR_GATE: FAIL` (if FAIL, do not output partial files; rewrite until PASS).

---

# Commercial-grade requirements (mandatory)

These sections exist to produce preflight output that is defensible under delivery disputes, security review, executive scope control, and pass/fail acceptance — not optional narrative.

## Mandatory Artifact: Decision Record (commercial-grade traceability)

In addition to the listed preflight artifacts, the pipeline must produce:

- `PREFLIGHT_DECISIONS.md` (human narrative)
- `PREFLIGHT_DECISIONS.json` (machine record)

These must capture, for each major architectural commitment:

- `decision_id`
- `decision_statement` (one sentence, testable)
- `alternatives_considered` (at least two real alternatives, not strawmen)
- `rejection_rationale_per_alternative` (specific, causal)
- `selected_rationale` tied to `purpose_claims` and `minimal_inevitable_set`
- `reversibility_cost_if_wrong`: `low` | `medium` | `high` with a concrete reason
- `owner_of_decision`: `user_explicit` | `inferred_high_confidence` | `inferred_low_confidence`

**Binary gate:** Phase 5 cannot approve if any decision has `reversibility_cost_if_wrong: high` while `owner_of_decision` is not `user_explicit`, unless there is a recorded `known_unknowns` entry with a mitigation plan tied to that decision.

**Rationale:** This artifact makes preflight output defensible in delivery disputes, security reviews, and executive scope control.

## Mandatory Section: Acceptance Criteria Packaging (pre-build, binary)

During Phase 3 (Minimal-Inevitable Architecture), define an acceptance package that becomes normative for later execution, without turning preflight into implementation.

Add artifacts:

- `PREFLIGHT_ACCEPTANCE.md`
- `PREFLIGHT_ACCEPTANCE.json`

**Minimum required content:**

- `acceptance_id` list (stable identifiers)
- Each criterion must be objectively verifiable (pass/fail); subjective checks (“looks good”) are forbidden
- Each criterion maps to at least one `purpose_claim`
- Explicit `non_goals` that are out of scope for acceptance

**Binary gate:**

- Cannot approve if fewer than **N** criteria, where **N = max(5, ceil(number_of_purpose_claims * 2))**.
- Cannot approve if any criterion references UI quality without specifying measurable proxies (e.g. routes exist, forms submit, error states exist, auth gates enforced), unless the project is explicitly non-UI.

**Rationale:** Converts opinion-based delivery fights into contractual pass/fail checks before expensive build labor.

## Mandatory Phase-2 Expansion: Expensive-Late-Failure Scan (ELS)

Phase 2 must include an explicit **ELS** section in `PREFLIGHT_ABSENCE_MAP.*`.

**ELS categories** (each must be addressed; use `not_applicable` only with a one-line proof):

- `security_abuse_and_threats` (authz/authn, tenancy, secrets, injection surfaces)
- `privacy_and_data_governance` (PII, retention, deletion, jurisdiction)
- `payments_and_money_movement` (if any)
- `operational_reliability` (SLO/DR/backups/monitoring hooks as **requirements**, not implementation)
- `accessibility_and_inclusive_design` (if any user-facing UI)
- `legal_and_policy_constraints` (licensing, export, industry rules) as applicable

**Output requirements:**

- `els_risks[]` each with: `risk`, `why_late_discovery_is_expensive`, `earliest_cheap_mitigation_stage` (`preflight` | `workspace_gen` | `execution`), `residual_open_risk` (boolean)

**Binary gate:**

- If `residual_open_risk: true` for any item under `payments_and_money_movement` or `privacy_and_data_governance`, Phase 5 cannot be `approved` unless status is `insufficient_information` **or** user-explicit acceptance is recorded in `PREFLIGHT_DECISIONS.json`.

**Rationale:** Prevents the class of failures that destroy budgets: building the wrong thing in a way that is not secure or compliant.

## Mandatory Phase-1 Output: Commercial Reality Invariants (CRI)

Phase 1 must extract and freeze commercial invariants as structured claims, separate from technical architecture.

Add to `PREFLIGHT_PURPOSE.json` (and summarize in `.md`):

- `target_customer_or_user_class`
- `primary_user_job_to_be_done` (single sentence)
- `business_outcome_hypothesis` (what improves if this succeeds)
- `monetization_model`: `none` | `subscription` | `usage` | `transaction_fee` | `ads` | `enterprise_contract` | `other`
- `must_have_constraints` (time/budget/compliance) as `user_stated` or `unknown`
- `kill_switch_triggers` (binary conditions that should stop the project)

**Binary rules:**

- If `monetization_model` is `unknown` for an intent that is clearly for-profit, Phase 5 must be `insufficient_information` until resolved **or** explicitly excluded with `non_goals` and user-explicit acknowledgment captured in decisions.

**Handoff rule:** Operator-like generation must treat CRI as non-negotiable unless preflight is reopened.

**Rationale:** Avoids generating impressive engineering workspaces for economically incoherent products.

---

# Anti-Drift Rules

Your file set must explicitly enforce these rules:

1. SKILL.md is the canonical runnable procedure.
2. `preflight-handoff.schema.json` is the canonical machine-readable contract source.
3. `contracts.md` explains the schema but does not replace it.
4. `phases.md` adds depth, anti-patterns, and drift prevention but does not become a duplicate skill.
5. `architecture.md` justifies the existence and system placement of the skill.
6. `integration-with-operator.md` owns the operator boundary, install/discovery rule, and conflict protocol.
7. If duplication would create maintenance drift, the duplicate content must be removed.

# Trigger Rules

You must ensure the new skill does not create ambiguous overlap with operator triggers.

Define a clean rule such as:
- the advanced agent identity always invokes preflight first for new workspace-generation requests
- direct operator usage remains legacy/basic path unless explicitly invoked
- workspace-architect does not compete with executor triggers
- workspace-architect is never the trigger for executing an already generated workspace

Make the trigger boundary unambiguous.

# Runtime Artifact Rules

The preflight process must write both:
- human-readable markdown
- machine-readable json

Explain exactly why both are needed.

Also define:
- cleanup or retention expectations for `v2/.buildr/preflight/<project-slug>/`
- whether a regenerated preflight reuses, overwrites, or versions previous artifacts
- whether approval artifacts must be immutable after approval unless preflight is re-opened
- how gitignore guidance applies to runtime staging folders

# Final Notes Section

At the very end of your response, include a concise implementation note listing:
- which existing repo files likely need later updates
- which parts are intentionally left unchanged in this step
- what assumptions you made about current Buildr structure
- which parts are v1 prompt-enforced versus future code-enforced
- how `v2/skills/` is expected to be installed or discovered at runtime
- whether `v2/.buildr/` should be gitignored by default
- what slugging/collision rule you chose and why

You should mention likely future updates to at least:
- README.md
- MANIFEST.md
- BUILDR_ARCHITECTURE.md
- existing operator docs or references
- forge/bridge integration points
- any install/copy instructions if users load prompts/skills into local CLI environments

You must include a subsection **Ground repo backlog (`v2/improve.md`)** in the Final implementation note:
- State that `v2/improve.md` is the canonical optional roadmap for integrating preflight with the rest of the repository (schemas, validation, ingest maps, vault, docs).
- List which backlog items (by section number or name) are **already reflected** in your generated files (e.g. `integration-with-operator.md`, `architecture.md`) versus **explicitly deferred** to post-merge work.
- If you deferred everything, say so in one explicit sentence — do not omit the subsection.

# Output Format

Return your answer in this exact order:

1. Brief architectural rationale
2. File tree
3. Full content of `v2/prompts/buildr-advanced-operator.md`
4. Full content of `v2/skills/buildr-workspace-architect/SKILL.md`
5. Full content of `v2/skills/buildr-workspace-architect/references/architecture.md`
6. Full content of `v2/skills/buildr-workspace-architect/references/phases.md`
7. Full content of `v2/skills/buildr-workspace-architect/references/contracts.md`
8. Full content of `v2/skills/buildr-workspace-architect/references/preflight-handoff.schema.json`
9. Full content of `v2/skills/buildr-workspace-architect/references/approval.md`
10. Full content of `v2/skills/buildr-workspace-architect/references/integration-with-operator.md`
11. Final implementation note
12. The single terminal line required by **Author Finalization Gate** (`AUTHOR_GATE: PASS` or `AUTHOR_GATE: FAIL`)

# Final Constraint

Do not output summaries of what you would write.
Do not output placeholders.
Do not output loose recommendations.
Output final file contents only.

**Exception:** Your response must end with exactly one line as required by **Author Finalization Gate** (`AUTHOR_GATE: PASS` or `AUTHOR_GATE: FAIL`).

Be exact.
Be exhaustive.
Every word must earn its place.