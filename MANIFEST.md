# Buildr System Manifest

> Auto-generated inventory of all system components.
> Update this file when adding or removing files.

---

## Engines (Python runtime)

- `engines/__init__.py` — Buildr Engines — the runtime core
- `engines/bridge.py` — Workspace builder: Forge + Index + Imperfektum + Vault selection
- `engines/forge_engine.py` — Onboarding, derivation, modules, scaffold generation
- `engines/imperfektum_engine.py` — Fabricated project memory generation
- `engines/vault_selector.py` — Stateless selector for vault skills, constraints, routines, memories
- `engines/preflight_validate.py` — v1.5 preflight artifact validator (binary gate)

## Skills (Agent capabilities)
- `skills/buildr-executor/SKILL.md` — buildr-executor: execute a Buildr workspace wave by wave to completion
- `skills/buildr-executor/references/architecture.md` — Executor state machine, file map, and Operator contrast
- `skills/buildr-operator/SKILL.md` — buildr-operator
- `skills/buildr-operator/references/preflight-ingest.md` — How operator ingests approved preflight artifacts
- `skills/buildr-rescue/SKILL.md` — buildr-rescue: import stuck/broken projects, diagnose, wrap, fix
- `skills/buildr-rescue/references/architecture.md` — Rescue overlay pattern, diagnosis engine
- `skills/buildr-scout/SKILL.md` — buildr-scout
- `skills/buildr-smith/SKILL.md` — buildr-smith
- `skills/buildr-workspace-architect/SKILL.md` — buildr-workspace-architect (v2): mandatory 5-phase preflight architecture gate
- `skills/buildr-workspace-architect/references/architecture.md` — System placement and anti-pattern justification
- `skills/buildr-workspace-architect/references/phases.md` — Phase depth, anti-patterns, drift prevention
- `skills/buildr-workspace-architect/references/contracts.md` — Inter-phase handoff contracts
- `skills/buildr-workspace-architect/references/preflight-handoff.schema.json` — Machine-readable payload schema (single source of truth)
- `skills/buildr-workspace-architect/references/approval.md` — Approval/rejection/insufficient semantics
- `skills/buildr-workspace-architect/references/integration-with-operator.md` — Operator boundary and install rule

## Vault — Skills (how to do things)
- `accessibility-check`
- `api-design`
- `auth-patterns`
- `code-review`
- `component-arch`
- `component-creation`
- `dark-mode`
- `data-fetch`
- `data-modeling`
- `database-schema`
- `deploy-checklist`
- `drag-drop`
- `environment-config`
- `error-boundary`
- `error-handling`
- `file-structure`
- `file-upload`
- `form-validation`
- `i18n`
- `input-sanitization`
- `logging-observability`
- `modal-dialog`
- `notification-system`
- `pagination`
- `payment-flow`
- `performance`
- `realtime-updates`
- `research`
- `responsive-layout`
- `search-filter`
- `seo`
- `state-design`
- `testing-strategy`

## Vault — Constraints (what not to do)
- `accessibility`
- `code-hygiene`
- `dependency-discipline`
- `no-console-log`
- `no-direct-db-in-ui`
- `no-empty-catch`
- `no-hardcoded-values`
- `no-implicit-any`
- `no-inline-styles`
- `no-magic-routes`
- `no-placeholder-content`
- `no-sync-in-async`
- `no-untyped-props`
- `performance`
- `security`
- `token-budget`

## Vault — Strategies (how to think)
- `build-order`
- `contract-first`
- `decomposition`
- `error-first`
- `error-vs-feature`
- `mobile-first`
- `progressive-enhancement`
- `scope-cut`
- `tech-choice`
- `test-scope`
- `when-to-abstract`
- `when-to-cache`

## Vault — Routines (verification)
- `accessibility-audit`
- `api-endpoint-check`
- `code-complete`
- `database-migration-check`
- `dependency-audit`
- `performance-check`
- `post-module-qa`
- `pre-commit`
- `pre-deploy`
- `responsive-verify`
- `retrospective`
- `security-check`
- `wave-handoff`

## Vault — Memories (Imperfektum templates)
- `vault/memories/universal-insights.md`
- `vault/memories/universal-scars.md`
- `vault/memories/category/api-memories.md`
- `vault/memories/category/booking.md`
- `vault/memories/category/dashboard-memories.md`
- `vault/memories/category/ecommerce.md`
- `vault/memories/category/saas.md`
- `vault/memories/category/tool.md`
- `vault/memories/category/webapp.md`
- `vault/memories/category/website.md`
- `vault/memories/stack/nextjs.md`
- `vault/memories/stack/prisma-memories.md`
- `vault/memories/stack/python.md`
- `vault/memories/stack/react-vite.md`
- `vault/memories/stack/static-html.md`
- `vault/memories/stack/typescript-memories.md`

## Memory System (Runtime memory)
- `memory-system/README.md` — Buildr Memory System quick start and feedback loop
- `memory-system/manifest.md` — Memory system tool manifest and rules
- `memory-system/config/defaults.json` — Runtime defaults for engine whitelist and injection markers
- `memory-system/config/defaults.yaml` — Reserved scalar defaults for `_common.sh`
- `memory-system/tools/_common.sh` — Shared Bash helpers for the memory system
- `memory-system/tools/wave-start.sh` — One-command wave start
- `memory-system/tools/wave-end.sh` — One-command wave end
- `memory-system/tools/discovery-write.sh` — Append discoveries with secret guards
- `memory-system/tools/discovery-distill.sh` — Distill discoveries into warm-tier summaries
- `memory-system/tools/discovery-mine.sh` — Mine git history into discoveries
- `memory-system/tools/context-load.sh` — Load hot/warm/cold context tiers
- `memory-system/tools/memory-inject.sh` — Inject discoveries into MEMORY.md
- `memory-system/tools/wave-brief.sh` — Generate hot-tier wave brief
- `memory-system/tools/wave-handoff.sh` — Generate wave handoff contract
- `memory-system/tools/wave-track.sh` — Track wave lifecycle metadata
- `memory-system/tools/checkpoint.sh` — Snapshot memory-system state
- `memory-system/tools/doctor.sh` — Validate memory-system health
- `memory-system/continuum/discoveries.jsonl` — Raw discovery log
- `memory-system/context/wave-brief.md` — Generated hot-tier context snapshot
- `memory-system/context/distilled.md` — Generated warm-tier distilled discoveries
- `memory-system/templates/circuit-breaker.md` — Rework circuit breaker registry
- `memory-system/templates/known-errors.md` — Shared known error registry
- `memory-system/templates/decisions.md` — Append-only architecture decisions log

## Templates (Orchestration kit)
- `templates/AGENT.md`
- `templates/CLAUDE.md`
- `templates/RUN.md`
- `templates/WORKSPACE.md`
- `templates/contracts/template.md`
- `templates/onboarding/prompt.md`
- `templates/state/orchestration.yaml`
- `templates/waves/000-template.md`

## V2 Preflight Layer
- `v2/prompts/buildr-advanced-operator.md` — Advanced agent identity with mandatory preflight
- `v2/skills/buildr-workspace-architect/SKILL.md` — Source-of-truth for the preflight skill
- `v2/skills/buildr-workspace-architect/references/*` — 6 reference files + JSON schema
- `v2/claude.md` — Canonical v2 authoring spec
- `v2/start.md` — Session bootstrap for v2 authoring
- `v2/improve.md` — Ground-repo hardening backlog

## Governance
- `docs/skill-governance.md` — Skill approval standard, classification decision tree, quality gates by type

## Plans & Docs
- `docs/plans/2026-03-27-structural-completion-design.md`
- `docs/plans/2026-03-27-structural-completion-implementation.md`
- `docs/plans/2026-03-27-skill-program.md` — Skill program backlog: 30+ items toward vault coverage targets
- `docs/BUILDR-purpose-and-layers.md` — Syfte, lager, specifikt vs strukturellt uppfyllande, agentens förslagsmandat, koppling till start/improve, prescriptiv generation (canonical; speglad i `v2/docs/`)
- `schemas/preflight/README.md` — Var canonical `preflight-handoff.schema.json` lever (ingen duplicerad fil i denna mapp)
- `templates/preflight/README.md` — Pekare till ingest-doc; policy om placeholders
- `v2/docs/README.md` — Index för v2/docs
- `v2/docs/purpose-and-layers.md` — Spegel av `docs/BUILDR-purpose-and-layers.md`
- `docs/v2-overview.md` — V2 preflight layer overview (flow, paths, install, v1 vs v2+)
- `docs/workspace-from-preflight.md` — Ingest map: preflight fields → workspace targets
- `docs/preflight-retention-policy.md` — Git, retention, immutability for preflight artifacts

## Tests
- `tests/__init__.py`
- `tests/test_bridge_integration.py`
- `tests/test_vault_selector.py`
- `tests/test_workspace_generation.py`
- `tests/test_preflight_validate.py` — preflight staging directory validator (v1.5 gate)

## Catalog (The Index)
- `catalog/index.json` — 11 indexed tools
- `catalog/meta/agent-rules.json`
- `catalog/meta/agent-skills-context-engineering.json`
- `catalog/meta/blueprint-forge.json`
- `catalog/meta/claude-code-router.json`
- `catalog/meta/claude-flow.json`
- `catalog/meta/claude-squad.json`
- `catalog/meta/constraint-mapper.json`
- `catalog/meta/opcode.json`
- `catalog/meta/pal-mcp-server.json`
- `catalog/meta/pipeline-composer.json`
- `catalog/meta/retrospective-builder.json`
- `catalog/meta/superclaude-framework.json`
- `catalog/meta/superpowers.json`
- `catalog/meta/ui-ux-pro-max-skill.json`
- `catalog/meta/vibe-kanban.json`

---

## Dependencies
- `requirements.txt` — Python dependencies (jsonschema for preflight validation)

---

**Total: ~210 files**
