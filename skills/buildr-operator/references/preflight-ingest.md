# Preflight Ingest — Operator Reference

When the advanced operator flow is active, workspace generation receives approved preflight artifacts as normative input. This file defines what the operator pipeline must respect.

---

## When This Applies

Only when `PREFLIGHT_APPROVAL.json` exists in `v2/.buildr/preflight/<slug>/` with `status: approved`. If no preflight artifacts exist, the operator runs its standard pipeline without constraints.

## Normative Fields

These preflight outputs constrain operator decisions:

| Source | Field | Operator Rule |
|--------|-------|--------------|
| `PREFLIGHT_PURPOSE.json` | `cri.target_customer_or_user_class` | Non-negotiable. Do not redefine target users. |
| `PREFLIGHT_PURPOSE.json` | `cri.monetization_model` | Non-negotiable. Drives payment module inclusion. |
| `PREFLIGHT_PURPOSE.json` | `cri.kill_switch_triggers` | Non-negotiable. Must be surfaced in PROJECT.md. |
| `PREFLIGHT_ARCHITECTURE.json` | `minimal_inevitable_set[]` | Normative. Every component must appear as a module. |
| `PREFLIGHT_ARCHITECTURE.json` | `non_goals[]` | Normative. Excluded capabilities stay excluded. |
| `PREFLIGHT_ACCEPTANCE.json` | `acceptance_criteria[]` | Binding. Each criterion → qa/acceptance.md item. |
| `PREFLIGHT_DECISIONS.json` | `decisions[]` | Normative. May not silently reverse. |
| `PREFLIGHT_ABSENCE_MAP.json` | `els_risks[]` with `stage: workspace_gen` | Must address during generation. |

## Conflict Protocol

If operator-like generation produces a decision that contradicts any normative field:

1. Stop generation.
2. Identify the conflict (which field, which artifact).
3. Present to user: reopen preflight or accept deviation (recorded as `user_explicit` decision).
4. Do not silently reinterpret.

Same protocol as defined in `v2/skills/buildr-workspace-architect/references/integration-with-operator.md`.

## What Operator Still Decides

Module decomposition, file structure, wave order, vault selection, design system, implementation patterns — all within approved architectural bounds.
