# Contracts Reference — Buildr Workspace Architect

## Purpose of Structured Handoffs

Each phase in the preflight pipeline produces artifacts that downstream phases consume. Structured handoffs ensure that:

1. **No information is lost between phases.** Phase 3 cannot ignore Phase 1's CRI fields because they are structured fields in a defined payload, not prose buried in a narrative.
2. **Drift is detectable.** If Phase 3's architecture serves a different user than Phase 1 specified, the structured `target_customer_or_user_class` field makes the discrepancy visible.
3. **Machine validation is possible.** Future v2+ code enforcement can validate payloads against `preflight-handoff.schema.json` without parsing natural language.
4. **Human review is efficient.** Markdown summaries let a human scan the analysis without parsing JSON. JSON payloads let tools validate without parsing prose.

---

## The Schema as Single Source of Truth

`preflight-handoff.schema.json` is the authoritative definition for all machine-readable payload structures.

### What the schema defines

- The shape of every JSON artifact produced by the pipeline.
- Required fields, allowed values, and type constraints.
- The approval payload structure (status, basis, rejections, missing inputs).
- CRI fields (Commercial Reality Invariants) for Phase 1.
- ELS risk structure (Expensive-Late-Failure Scan) for Phase 2.
- Acceptance criteria structure for Phase 3.
- Decision record structure for Phase 4.

### What the schema does not define

- The narrative structure of markdown artifacts. Markdown is human-facing and does not require schema validation.
- The reasoning process within each phase. The schema defines outputs, not procedures.
- The sequencing of phases. Phase order is defined in `SKILL.md`.

### Rule: No contradiction

If this file (`contracts.md`) describes a payload structure that differs from `preflight-handoff.schema.json`, the schema is authoritative and this file is wrong. This file explains the schema; it does not replace it.

---

## How Markdown Summaries and JSON Payloads Relate

Every phase produces both a `.md` and a `.json` artifact (except `PREFLIGHT_BUILD_ORDER.md`, which is markdown only).

| Artifact Type | Audience | Purpose |
|--------------|----------|---------|
| `.md` | Human reviewers, stakeholders | Readable narrative with context, reasoning, and rationale |
| `.json` | Downstream phases, future code validation, workspace generation | Structured data for machine consumption |

### Consistency rule

The JSON payload is the programmatic truth. The markdown narrative must not contradict the JSON payload. If a human reviewer reads the markdown and the JSON tells a different story, the JSON is correct and the markdown must be updated.

In practice, the agent writes both simultaneously from the same analysis. Divergence is a bug, not a design feature.

### What markdown adds beyond JSON

- Explanatory context: why a decision was made, not just what was decided.
- Narrative flow: how the analysis progressed, what was considered and discarded.
- Human-readable formatting: tables, lists, emphasis for key points.
- Qualitative nuance that does not reduce to structured fields.

### What JSON adds beyond markdown

- Machine-parseable structure for automated validation.
- Stable field names for cross-phase references (e.g., Phase 3 referencing Phase 1's `purpose_claims` by array index or claim text).
- Schema-validatable payloads for future v2+ code enforcement.
- Deterministic structure for diffing between preflight runs.

---

## What Each Phase Must Carry Forward

### Phase 1 -> Phase 2

Phase 2 reads `PREFLIGHT_PURPOSE.json` and uses:

| Field | How Phase 2 Uses It |
|-------|-------------------|
| `purpose_claims[]` | Each claim is checked for associated absences |
| `assumptions[]` | Each assumption is assessed: what if wrong? |
| `exclusions[]` | Exclusions are noted — absences within excluded scope are not flagged |
| `target_customer_or_user_class` | Informs ELS analysis (e.g., consumer vs. enterprise affects privacy requirements) |
| `monetization_model` | Informs ELS analysis (e.g., `transaction_fee` triggers `payments_and_money_movement` deep analysis) |
| `kill_switch_triggers[]` | Absences related to kill-switch conditions are flagged as `blocking` |

### Phase 2 -> Phase 3

Phase 3 reads `PREFLIGHT_PURPOSE.json` and `PREFLIGHT_ABSENCE_MAP.json` and uses:

| Field | How Phase 3 Uses It |
|-------|-------------------|
| `purpose_claims[]` | Each claim must be satisfied by at least one architectural component |
| `known_unknowns[]` | Architecture must not depend on unresolved unknowns for core functionality |
| `els_risks[]` | Risks with `earliest_cheap_mitigation_stage: workspace_gen` must be addressed in architecture |
| `absences[]` with `classification: blocking` | Must have been resolved or pipeline would have terminated |
| `absences[]` with `classification: derivable` | Phase 3 may resolve these through architectural decisions (recorded in decisions) |
| CRI fields | `monetization_model` informs whether payment architecture is in the minimal set |

### Phase 3 -> Phase 4

Phase 4 reads all prior outputs and uses:

| Field | How Phase 4 Uses It |
|-------|-------------------|
| `minimal_inevitable_set[]` | Each component is challenged: is it truly inevitable? |
| `non_goals[]` | Each exclusion is challenged: is it safe to exclude? |
| `acceptance_criteria[]` | Each criterion is assessed: is it genuinely verifiable? |
| `purpose_claims[]` | Challenge tests components against purpose — does this component serve the stated purpose? |
| `els_risks[]` with `residual_open_risk: true` | Each residual risk is challenged: is the mitigation sufficient? |

### Phase 4 -> Phase 5

Phase 5 reads all prior outputs and uses:

| Field | How Phase 5 Uses It |
|-------|-------------------|
| `decisions[]` | Verified: all have `alternatives_considered >= 2`, no ungated high-risk decisions |
| `challenged_components[]` | Input to approval basis: which components survived challenge |
| `open_risks[]` | Carried into approval as acknowledged risks |
| All prior phase completion statuses | Each gate is re-verified before approval determination |
| `monetization_model` | Gate: `unknown` for for-profit -> `insufficient_information` unless excluded |
| `els_risks[]` under payments/privacy | Gate: `residual_open_risk: true` -> blocks approval without user acceptance |

---

## How Rejection, Insufficiency, and Approval Are Represented

### In JSON (`PREFLIGHT_APPROVAL.json`)

```
status: "approved"
  -> approval_basis: [non-empty array of evidence strings]
  -> allowed_next_step: "workspace_generation"
  -> open_risks: [array, may be empty]
  -> non_goals: [array, at least one entry]
  -> minimal_inevitable_set: [array of confirmed components]

status: "rejected"
  -> rejection_reasons: [non-empty array of specific reasons]
  -> allowed_next_step: "rerun_preflight" | "project_cancelled"

status: "insufficient_information"
  -> required_missing_inputs: [non-empty array of specific missing items]
  -> allowed_next_step: "user_input_required"
```

### In Markdown (`PREFLIGHT_APPROVAL.md`)

The markdown narrative provides context for the determination:
- For `approved`: what evidence supports approval, what risks are acknowledged.
- For `rejected`: what specifically failed, what would need to change.
- For `insufficient_information`: what information is missing, why it matters, what questions to ask the user.

---

## How Drift Is Prevented Between Prose and Schema

### Rule 1: Schema is authoritative

If the markdown says one thing and the JSON says another, the JSON is correct. The markdown must be updated to match.

### Rule 2: Artifacts are written simultaneously

The agent writes both `.md` and `.json` from the same analysis in the same phase execution. There is no temporal gap in which drift can occur during initial creation.

### Rule 3: Cross-phase references use JSON fields

When Phase 3 references Phase 1's purpose claims, it references the structured `purpose_claims[]` array in `PREFLIGHT_PURPOSE.json`, not a paragraph in the markdown. This ensures the reference is to a stable, structured field.

### Rule 4: Schema validation catches structural drift

In v2+ code enforcement, `preflight-handoff.schema.json` validation will catch:
- Missing required fields.
- Invalid field values (e.g., `status: "maybe"`).
- Type mismatches (e.g., `purpose_claims` as a string instead of an array).
- Empty arrays where non-empty is required.

### Rule 5: No field is defined only in prose

Every structured field referenced by the pipeline must exist in `preflight-handoff.schema.json`. If a field appears in `contracts.md` or `SKILL.md` but not in the schema, the schema is incomplete and must be updated. Prose-only fields are not part of the contract.
