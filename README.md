# Buildr

From a conversation to a complete, agent-built product.

## What This Is

A system that takes a human project description and produces a self-contained
workspace that any LLM agent can autonomously execute to build the project.

The system combines five components:

- **Forge** — Onboarding + scaffold generation
- **Vault** — 100 reusable, project-agnostic building blocks
- **Orchestration** — Wave-based execution with progressive disclosure
- **Imperfektum** — Fabricated agent memories that prevent common mistakes
- **Index** — Catalog of all tools and capabilities

Runtime memory operations live in `memory-system/`, which adds discovery logging,
context tier loading, handoffs, checkpoints, and MEMORY.md injection for Buildr agents.

## Quick Start

### Option A: Use with Claude Code / agent CLI

```bash
# Copy skills to your agent's skill directory
cp -r skills/buildr-operator/ .claude/skills/
cp -r skills/buildr-smith/ .claude/skills/

# Tell your agent:
# "I want to build a booking site for fishing trips in Zanzibar"
# The operator skill handles the rest.
```

### Option B: Use the Python engines directly

```bash
cd engines/
python bridge.py
# Follow the prompts → workspace generated
```

### Option C: Point an agent at a generated workspace

```bash
# After generating a workspace:
cd my-project-workspace/
# Tell your agent: "Read WORKSPACE.md, then follow AGENT.md"
```

## Directory Structure

```text
buildr/
├── README.md                  ← You are here
├── BUILDR_ARCHITECTURE.md     ← System design document
├── memory-system/             ← Runtime memory + context tooling
│
├── engines/                   ← Python engines
│   ├── forge_engine.py           Onboarding → scaffold
│   ├── imperfektum_engine.py     Memory generation
│   └── bridge.py                 Connects everything
│
├── skills/                    ← Agent skills
│   ├── buildr-operator/          "I want to build X" → workspace
│   └── buildr-smith/             Create/maintain Vault items
│
├── vault/                     ← Reusable building blocks (95% of agent knowledge)
│   ├── skills/                   How to do things
│   ├── constraints/              What not to do
│   ├── strategies/               How to think about decisions
│   ├── routines/                 Verification checklists
│   └── memories/                 Imperfektum templates
│
├── catalog/                   ← The Index (tool catalog)
│   ├── index.json
│   └── meta/
│
├── references/                ← Forge reference data
│   └── category-modules.md
│
└── templates/                 ← Orchestration kit templates
    ├── CLAUDE.md
    ├── RUN.md
    ├── onboarding/
    ├── state/
    ├── waves/
    └── contracts/
```

## Prerequisites

- Python ≥ 3.10
- An LLM agent (Claude Code, Codex, Gemini CLI, or any capable agent)

## How It Works

1. You describe what you want to build (human language, no technical terms)
2. The system derives all technical decisions (never asks)
3. It generates a workspace folder with everything the agent needs
4. The agent reads the workspace and builds the project autonomously
5. Each build phase uses relevant Vault items and fresh Imperfektum memories
6. Quality gates after every module prevent cascading errors

See `BUILDR_ARCHITECTURE.md` for the full system design.

## License

Proprietary — buildr.nu
# BlLdR
