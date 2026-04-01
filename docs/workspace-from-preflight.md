# Workspace from Preflight — Ingest Map

How preflight artifacts drive workspace generation. Each row maps a preflight field to the workspace file/section it populates.

---

## CRI → PROJECT.md

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `cri.target_customer_or_user_class` | PROJECT.md "Target Users" | Verbatim — non-negotiable |
| `cri.primary_user_job_to_be_done` | PROJECT.md "Core Purpose" | Verbatim — non-negotiable |
| `cri.business_outcome_hypothesis` | PROJECT.md "Success Metric" | Verbatim — non-negotiable |
| `cri.monetization_model` | PROJECT.md "Constraints" + module selection | Drives payment/billing module inclusion |
| `cri.must_have_constraints` | PROJECT.md "Hard Constraints" | Each constraint becomes a project constraint |
| `cri.kill_switch_triggers` | PROJECT.md "Kill Switches" | Verbatim — binary stop conditions |

## Minimal-Inevitable Set → Modules + Waves

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `minimal_inevitable_set[]` | `modules/*.md` | Each component becomes at least one module spec |
| Component `classification: core` | Wave ordering (early waves) | Core components are built first |
| Component `classification: supporting` | Wave ordering (later waves) | Supporting components follow core |
| `PREFLIGHT_BUILD_ORDER.md` | `waves/001-*.md` ordering | Recommended build sequence → wave plan input |

## Acceptance Criteria → QA

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `acceptance_criteria[]` | `qa/acceptance.md` | Each `AC-NNN` → QA checklist item (binary pass/fail) |
| `acceptance_criteria[].purpose_claim_refs` | `qa/acceptance.md` traceability | Each QA item references its purpose claim |
| `non_goals_for_acceptance[]` | `qa/acceptance.md` "Out of Scope" | Explicit exclusions from QA |

## Decisions → State + Contracts

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `decisions[]` | `state/orchestration.yaml` `decisions:` | Each `DEC-NNN` → decision entry in state |
| `decisions[].decision_statement` | `contracts/*.md` (where relevant) | Architectural decisions become contract constraints |
| `decisions[].reversibility_cost_if_wrong` | Risk annotations in wave specs | High-cost decisions flagged in relevant waves |

## ELS Risks → Modules + QA

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `els_risks[]` with `stage: workspace_gen` | Module specs + vault selection | Risk mitigation baked into module requirements |
| `els_risks[]` with `stage: execution` | Wave specs | Flagged as execution-time concerns in relevant waves |
| `els_risks[]` with `residual_open_risk: true` | `qa/acceptance.md` "Open Risks" | Tracked but not blocking QA (already accepted) |

## Absence Map → Vault Selection

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `absences[]` with `classification: derivable` | Operator derivation input | Resolved absences inform technical derivation |
| `known_unknowns[]` | `state/orchestration.yaml` `backlog:` | Tracked for potential mid-build resolution |

## Purpose Claims → Everywhere

| Preflight Field | Workspace Target | How |
|-----------------|-----------------|-----|
| `purpose_claims[]` | PROJECT.md, qa/acceptance.md, modules/ | Thread through all workspace artifacts as the "why" |

---

## What Is NOT Ingested

- Phase 4 challenge details (internal analysis, not workspace content)
- Phase 2 absence analysis prose (consumed by preflight, not by workspace)
- `PREFLIGHT_BUILD_ORDER.md` narrative (only the ordering is used)

## Future: Machine-Readable Bindings

A `catalog/preflight-bindings.json` mapping `purpose_claims` / categories to vault skill-ids would automate vault selection from preflight. Deferred until automated sync against `vault/INDEX.md` exists to prevent stale references.
