# Buildr Operator — Architecture Reference

> For the complete system architecture, see `BUILDR_ARCHITECTURE.md` at repo root.
> This file covers only Operator-specific architectural decisions.

## Operator's Place in the System

The Operator is the **entry point** for new projects. It sits between
the human (who describes what they want) and the Executor (who builds it).

```
Human → Operator → Workspace → Executor → Finished Project
```

The Operator does NOT build anything. It produces the workspace that
contains everything needed for any agent to build the project.

## What Operator Generates

```
project-workspace/
├── CLAUDE.md              ← Orchestration protocol (from templates/)
├── WORKSPACE.md           ← Master overview
├── PROJECT.md             ← What to build, hard constraints
├── SYSTEM.md              ← Design system, code standards
├── MEMORY.md              ← Imperfektum: fabricated agent memories
├── TOOLS.md               ← Available tools
├── AGENT.md               ← Builder agent protocol
├── EVALUATOR.md           ← Reviewer protocol
├── RUN.md                 ← Execution entrypoint with quality gates
├── agents/                ← Derived agent team (manifest + per-agent .md)
├── state/orchestration.yaml ← Progress tracking with current/next wave
├── waves/001-foundation.md  ← First wave
├── contracts/             ← Interface contracts
├── modules/               ← Per-module specifications
├── qa/
│   ├── checklist.md       ← Per-module binary checks
│   ├── acceptance.md      ← Definition of "done"
│   └── gates.md           ← 3-phase quality gates
├── vault-selection/       ← Vault items selected for wave 001
└── spec.json              ← Machine-readable project spec
```

## Derivation Chain

```
User answers (natural language)
  → ProjectSpec (structured data)
    → ProjectBlueprint (spec + design + modules + phases)
      → ScaffoldGenerator (blueprint → files)
        → Agent team (category → team via TEAM_MAP)
          → Complete workspace
```

## Key Design Decisions

1. **Never ask technical questions.** All tech decisions are derived.
2. **Only Wave 1 is planned.** Later waves are organic.
3. **Agent team is derived from category.** web-app gets 7 agents, tool gets 5.
4. **CLAUDE.md is the source of truth** for execution protocol.
5. **Registry integration** — Operator registers projects after generation.
