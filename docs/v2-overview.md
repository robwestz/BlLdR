# Buildr v2 — Preflight Architecture Layer

One-page overview of the v2 system layer.

---

## What v2 Adds

A mandatory preflight pipeline that runs before workspace generation. One human description → five architecture phases → structured approval → workspace generation within approved bounds.

```
Human description
    |
    v
[buildr-workspace-architect]   Preflight: 5 phases, binary gates
    |
    v  PREFLIGHT_APPROVAL.json (status: approved)
    |
[operator-like generation]     Existing operator pipeline (Phases 2-5)
    |
    v  Generated workspace
    |
[buildr-executor]              Unchanged
```

## Key Files

| File | Purpose |
|------|---------|
| `v2/prompts/buildr-advanced-operator.md` | System prompt for the advanced flow |
| `v2/skills/buildr-workspace-architect/SKILL.md` | The preflight skill (5 phases) |
| `v2/skills/.../references/preflight-handoff.schema.json` | Single source of truth for JSON payloads |
| `v2/skills/.../references/architecture.md` | Why this is a system skill |
| `v2/skills/.../references/phases.md` | Phase depth and anti-patterns |
| `v2/skills/.../references/contracts.md` | Inter-phase handoff contracts |
| `v2/skills/.../references/approval.md` | Approval/rejection/insufficient semantics |
| `v2/skills/.../references/integration-with-operator.md` | Operator boundary and install rule |
| `v2/improve.md` | Ground-repo backlog (post-v2 hardening) |
| `engines/preflight_validate.py` | v1.5 binary gate (CLI validator) |

## Staging Path

Preflight artifacts are written to:
```
v2/.buildr/preflight/<project-slug>/
```
This path is gitignored by default (see `.gitignore`).

## Install / Discovery

`v2/skills/` is the source-of-truth in-repo path. For runtime discovery:

```bash
# Copy to runtime skill directory (Windows-safe)
cp -r v2/skills/buildr-workspace-architect skills/buildr-workspace-architect
```

After installation, load `v2/prompts/buildr-advanced-operator.md` as the agent's system prompt.

## v1 vs v2+

| Aspect | v1 (current) | v2+ (future) |
|--------|-------------|-------------|
| Gate enforcement | Agent reads prompt, follows rules | Code in forge/bridge validates schema |
| Bypass risk | Possible (agent error) | Impossible (code blocks) |
| Validation | `engines/preflight_validate.py` (CLI) | Integrated into `forge_engine.py` |

## Legacy vs Advanced Flow

| Flow | Entry Point | Preflight? |
|------|-------------|-----------|
| **Legacy/basic** | `buildr-operator` skill directly | No |
| **Advanced** | `buildr-advanced-operator.md` prompt | Yes (mandatory) |

Both flows are valid. The advanced flow adds preflight gating. The legacy flow remains available for users who want direct workspace generation.

## Canonical Spec

The authoritative spec for v2 content is `v2/claude.md`. Other copies (`v2-codex/`, `v2-gemini/`, etc.) are tool-session artifacts and may diverge.

## Related Docs

- `docs/workspace-from-preflight.md` — How preflight artifacts drive workspace generation
- `docs/preflight-retention-policy.md` — Git, retention, and immutability rules
- `skills/buildr-operator/references/preflight-ingest.md` — Operator's view of preflight
- `vault/strategies/preflight-reopen.md` — When and how to reopen approved preflight
- `vault/routines/preflight-gate-check.md` — Binary gate check before generation
