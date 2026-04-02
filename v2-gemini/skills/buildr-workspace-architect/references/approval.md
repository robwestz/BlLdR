# Approval Reference — Buildr Workspace Architect

## What "Approved" Means Operationally

`status: approved` in `PREFLIGHT_APPROVAL.json` means ALL of the following are true:

1. **Phase 1 gate passed.** All CRI fields are populated. At least one falsifiable purpose claim exists. `target_customer_or_user_class` is specific (not "users" or "everyone").
2. **Phase 2 gate passed.** All six ELS categories are addressed. No unaddressed blocking absences remain.
3. **Phase 2 ELS gate passed.** No `residual_open_risk: true` under `payments_and_money_movement` or `privacy_and_data_governance` without either `insufficient_information` status or user-explicit acceptance in `PREFLIGHT_DECISIONS.json`.
4. **Phase 3 gate passed.** Acceptance criteria count meets `max(5, ceil(purpose_claims * 2))`. All criteria are objectively verifiable. All criteria map to at least one purpose claim.
5. **Phase 4 decision gate passed.** No decision has `reversibility_cost_if_wrong: high` with `owner_of_decision` not `user_explicit`, unless a `known_unknowns` entry with a mitigation plan is tied to that decision.
6. **Phase 1 monetization gate passed.** If `monetization_model: unknown` for a clearly for-profit intent, status is `insufficient_information` — not `approved` — unless the monetization question is explicitly excluded via `non_goals` with user-explicit acknowledgment in decisions.
7. **`approval_basis` is non-empty.** At least one evidence string explains why approval is warranted.
8. **All required artifacts exist** in the staging directory (see artifact list in `SKILL.md`).
9. **`allowed_next_step` is `workspace_generation`.** This is the only valid next step for an approved preflight.

### What approval authorizes

- Workspace generation may proceed using operator-like generation.
- The minimal-inevitable set is the normative architectural foundation.
- CRI fields are non-negotiable inputs to generation.
- Acceptance criteria are binding for the generated workspace's QA.
- Decision records are normative — generation may not silently reverse them.

### What approval does NOT authorize

- Execution of the generated workspace (that requires executor).
- Deviation from the approved architecture without triggering the conflict protocol.
- Addition of components not in the minimal-inevitable set without explicit justification recorded in decisions.
- Removal of acceptance criteria.
- Reinterpretation of CRI fields.

---

## What "Rejected" Means Operationally

`status: rejected` in `PREFLIGHT_APPROVAL.json` means at least one of the following is true:

1. **A phase produced irreconcilable contradictions.** Two or more purpose claims require mutually exclusive architectural components with no resolution path.
2. **The purpose is incoherent.** The description contains contradictions that prevent meaningful architecture.
3. **A mandatory architectural component is impossible** given stated constraints (time, budget, technology, compliance).
4. **Phase 4 challenge revealed fundamental flaws** with no resolution path — the architecture is not adjustable, it is wrong.
5. **A binary gate failed with no remediation.** For example, Phase 3 cannot produce enough verifiable acceptance criteria from the stated purpose.

### What rejection means for the user

- The project cannot proceed to workspace generation in its current form.
- The user must revise the project description to address `rejection_reasons`.
- A revised description triggers a new preflight run from Phase 1.
- Rejection is not permanent — it applies to this specific description.

### What rejection does NOT mean

- It does not mean the project idea is bad. It means the description, as given, cannot produce a defensible architecture.
- It does not mean the user must abandon the project. It means specific issues must be resolved.

### Operational action on rejection

1. Present `rejection_reasons` to the user with specificity.
2. Explain which binary gate failed and why.
3. If the user provides a revised description: rerun preflight from Phase 1 (new run, same or new slug).
4. `allowed_next_step` is `rerun_preflight` or `project_cancelled`.

---

## What "Insufficient Information" Means Operationally

`status: insufficient_information` in `PREFLIGHT_APPROVAL.json` means:

1. **The project is potentially viable** but the current description lacks information required by one or more binary gates.
2. **Specific inputs are identified** in `required_missing_inputs` — these are not vague requests but precise questions.
3. **The pipeline terminated early** because a blocking absence or unresolvable gate prevented progression.

### Difference from rejection

| Dimension | Rejected | Insufficient Information |
|-----------|---------|------------------------|
| Project viability | Questionable — contradictions or impossibility | Potentially viable — just needs more data |
| User action | Revise the concept | Answer specific questions |
| Preflight rerun | From Phase 1 with revised description | From Phase 1 with augmented description |
| Tone | "This doesn't work because X" | "I need to know X before I can determine if this works" |

### Common triggers for insufficient_information

- CRI `monetization_model: unknown` for a clearly for-profit project.
- Blocking absence in Phase 2 that requires user input (e.g., "Which payment provider?" for a transaction-fee project).
- ELS risk with `residual_open_risk: true` under payments or privacy without user-explicit acceptance.
- Target user class too vague to derive architectural constraints.

### Operational action on insufficient_information

1. Present `required_missing_inputs` to the user as specific questions.
2. For each missing input, reference which phase and which gate requires it.
3. Wait for user response.
4. Rerun preflight from Phase 1 with the original description augmented by user responses.
5. `allowed_next_step` is `user_input_required`.

---

## What Must Exist Before Generation Is Allowed

Generation is blocked unless ALL of the following conditions are met:

1. `PREFLIGHT_APPROVAL.json` exists in `v2/.buildr/preflight/<project-slug>/`.
2. `PREFLIGHT_APPROVAL.json` has `status: approved`.
3. `PREFLIGHT_APPROVAL.json` has `approval_basis` with at least one entry.
4. `PREFLIGHT_APPROVAL.json` has `allowed_next_step: workspace_generation`.
5. `PREFLIGHT_APPROVAL.json` has `gates_verified` with all six gates set to `true`.
6. All 15 required artifacts exist in the staging directory (see `SKILL.md` artifact table).

If any condition is not met, generation is blocked regardless of any other signal.

---

## What Must Never Happen After Approval

Once `status: approved` is written to `PREFLIGHT_APPROVAL.json`:

1. **Preflight artifacts are immutable.** No file in the staging directory may be modified unless preflight is explicitly reopened.
2. **CRI fields may not be reinterpreted.** If `target_customer_or_user_class` says "tourists visiting Zanzibar," the workspace may not target "business travelers."
3. **Architectural components may not be silently added or removed.** Changes to the minimal-inevitable set require the conflict protocol.
4. **Acceptance criteria may not be dropped.** Every criterion in `PREFLIGHT_ACCEPTANCE.json` must appear in the generated workspace's QA checklist.
5. **Decision records may not be silently reversed.** Reversing a decision requires the conflict protocol and a new decision record with `owner_of_decision: user_explicit`.

---

## Re-Open Conditions

Preflight may be reopened (triggering a new run) under these conditions:

1. **User explicitly requests it.** The user says "redo preflight" or equivalent. A new run starts from Phase 1.
2. **Conflict protocol triggers re-open.** Operator-like generation detects a conflict with approved preflight and the user chooses to reopen rather than accept the deviation.
3. **Material new information.** The user provides information that materially changes the purpose or constraints after approval. The agent explains that this requires reopening preflight and waits for user confirmation.

### What reopening does

- A new preflight run begins from Phase 1 with the augmented/revised input.
- The previous approved artifacts are preserved under their existing slug (or a new timestamped slug is created per collision rules).
- The new run produces a new set of artifacts.
- The previous approval has no bearing on the new run — each run is independent.

### What reopening does NOT do

- It does not modify existing approved artifacts.
- It does not create an "amendment" to the existing approval. Each approval is atomic and complete.
- It does not allow selective re-running of individual phases. Reopening means Phase 1 through Phase 5.

---

## Conflict Protocol

When operator-like generation detects that a workspace decision contradicts an approved preflight artifact:

1. **Stop immediately.** Do not continue building on a conflicted foundation.
2. **Identify the conflict.** Name the specific artifact, field, and value that is contradicted.
3. **Present two options to the user:**
   - **Reopen preflight:** Rerun from the phase whose output is contradicted. All downstream phases rerun.
   - **Accept deviation:** User explicitly acknowledges. Record as a new decision in `PREFLIGHT_DECISIONS.json` with `owner_of_decision: user_explicit`.
4. **Do not silently resolve.** The agent may not reinterpret approved artifacts to make the conflict disappear.
5. **Do not continue generation** until the conflict is resolved through one of the two paths.

---

## Challenge-Loop Closure Rule

Phase 4 performs exactly one challenge pass. This is a design decision, not a limitation:

- **Items that survive challenge:** Confirmed. Recorded in decisions.
- **Items that fail challenge:** Adjusted (with decision record) or escalated to open risks.
- **Unresolved items:** Carried as `known_unknowns` with `open_risks` entries.

There is no iteration between Phase 3 and Phase 4. If the architecture is fundamentally flawed, the correct response is `rejected`, not another pass.

Rationale: The architecture at this stage is minimal-inevitable — it is the smallest possible set. Further iteration optimizes or rearranges, but a minimal set either works or it does not. If it does not, the problem is in the purpose or constraints, not in the arrangement of components.

---

## The Exact Meaning of the Preflight Gate in v1

In v1 (current implementation), the preflight gate is **prompt-enforced**:

- The advanced operator prompt instructs the agent to check `PREFLIGHT_APPROVAL.json` before proceeding to generation.
- The agent reads the file, parses the `status` field, and blocks or proceeds accordingly.
- There is no code in forge or bridge that validates this check.
- Compliance depends entirely on the agent following the prompt.
- A well-instructed agent will never bypass the gate. A misconfigured or custom agent might.

### The risk of prompt-only enforcement

- An agent without the advanced operator prompt loaded will not check for preflight.
- An agent under context pressure (long conversation, many tool calls) might skip the check.
- A deliberately modified prompt could bypass the gate.

These risks are acceptable for v1 because:
- The advanced operator prompt is the only entry point for the advanced flow.
- Basic operator usage (without preflight) remains a valid, separate flow.
- The risk of accidental bypass is low in normal usage.

---

## What Future Code-Enforced Gating Should Check in v2+

When forge/bridge gain preflight validation, the code should verify:

1. **Existence check:** `v2/.buildr/preflight/<slug>/PREFLIGHT_APPROVAL.json` exists.
2. **Schema validation:** The file validates against the `approval_payload` definition in `preflight-handoff.schema.json`.
3. **Status check:** `status` field is `approved`.
4. **Basis check:** `approval_basis` array is non-empty.
5. **Next step check:** `allowed_next_step` is `workspace_generation`.
6. **Gates check:** All six entries in `gates_verified` are `true`.
7. **Artifact completeness:** All 15 required files exist in the staging directory.
8. **Cross-reference check:** `PREFLIGHT_ACCEPTANCE.json` criteria are present and count meets the minimum formula.
9. **Decision integrity check:** No decision in `PREFLIGHT_DECISIONS.json` has `reversibility_cost_if_wrong: high` with non-`user_explicit` owner without a linked mitigation in `known_unknowns`.

Any check failure blocks `forge_engine.py` from executing workspace generation. The error message references the specific check that failed.
