# Buildr

From a conversation to a complete, agent-built product.

> **"95% of what makes an agent effective is project-agnostic."**
> Buildr separates the reusable 95% from the project-specific 5%,
> so any LLM agent can autonomously build any software project.

---

## What This Is

A system that takes a human project description and produces a self-contained
workspace that any LLM agent can autonomously execute to build the project.

The system combines six components:

| Component | Purpose |
|-----------|---------|
| **Forge** | Onboarding + scaffold generation |
| **Vault** | 90 reusable, project-agnostic building blocks |
| **Orchestration** | Wave-based execution with progressive disclosure |
| **Imperfektum** | Fabricated agent memories that prevent common mistakes |
| **Index** | Catalog of all tools and capabilities |
| **Memory System** | Runtime discovery logging, context tiers, wave tracking |

**Purpose, layers & agent intent:** why Buildr is more than “a workspace folder”, how **specific** and **structural** work can both fulfill the same user goal, and how agents should reason from **repo capability → intent** — see **`docs/BUILDR-purpose-and-layers.md`** (mirror: `v2/docs/purpose-and-layers.md`).

## Quick Start

### Option A: Use with Claude Code / agent CLI (basic flow)

```bash
# Copy skills to your agent's skill directory
cp -r skills/buildr-operator/ ~/.claude/skills/
cp -r skills/buildr-executor/ ~/.claude/skills/
cp -r skills/buildr-smith/ ~/.claude/skills/
cp -r skills/buildr-scout/ ~/.claude/skills/

# Tell your agent:
# "I want to build a booking site for fishing trips in Zanzibar"
# The operator skill handles the rest.
```

### Option A2: Advanced flow (with preflight architecture gate)

```bash
# Install v2 skill
cp -r v2/skills/buildr-workspace-architect/ skills/buildr-workspace-architect/

# Load the advanced operator prompt as system prompt
# (v2/prompts/buildr-advanced-operator.md)
# This adds mandatory 5-phase preflight before workspace generation.
# See docs/v2-overview.md for details.
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

## Agent Skills

| Skill | Role |
|-------|------|
| **buildr-operator** | Takes a human idea → produces a complete workspace |
| **buildr-executor** | Executes a workspace wave by wave to completion |
| **buildr-smith** | Creates and maintains Vault items (the building blocks) |
| **buildr-scout** | Extracts knowledge from external sources → system improvements |
| **buildr-rescue** | Takes a stuck/broken project → diagnoses → wraps → fixes |
| **buildr-workspace-architect** | (v2) Mandatory preflight: 5-phase architecture gate before generation |

## Directory Structure

```text
buildr/
├── README.md                  ← You are here
├── BUILDR_ARCHITECTURE.md     ← Full system design document
├── MANIFEST.md                ← Complete system inventory
│
├── schemas/preflight/         ← README: where canonical preflight JSON Schema lives (no duplicate file)
│
├── engines/                   ← Python runtime
│   ├── forge_engine.py           Onboarding → scaffold
│   ├── imperfektum_engine.py     Fabricated memory generation
│   ├── vault_selector.py         Vault item selection per wave
│   └── bridge.py                 Connects everything
│
├── v2/                        ← V2 preflight architecture layer
│   ├── ENTRY.md                  **Start here** — menu of v2 options (or run v2/run.ps1)
│   ├── run.ps1                   Interactive menu (Windows PowerShell)
│   ├── prompts/                  Advanced operator prompt
│   ├── skills/                   Workspace architect skill + references
│   ├── docs/                     purpose-and-layers (mirror of docs/BUILDR-purpose-and-layers.md)
│   └── improve.md                Ground-repo hardening backlog
│
├── skills/                    ← Agent skills (6)
│   ├── buildr-operator/          "I want to build X" → workspace
│   ├── buildr-executor/          Workspace → finished build
│   ├── buildr-smith/             Create/maintain Vault items
│   ├── buildr-scout/             Knowledge extraction → system evolution
│   └── buildr-rescue/            Stuck project → diagnose → wrap → fix
│
├── vault/                     ← Reusable building blocks (90 items)
│   ├── skills/                   How to do things (33)
│   ├── constraints/              What not to do (16)
│   ├── strategies/               How to think about decisions (12)
│   ├── routines/                 Verification checklists (13)
│   └── memories/                 Imperfektum templates (16)
│
├── memory-system/             ← Runtime memory
│   ├── tools/                    13 bash scripts (wave lifecycle, discoveries)
│   ├── continuum/                Discovery log + sessions + checkpoints
│   ├── context/                  Generated wave briefs
│   └── config/                   Runtime defaults
│
├── catalog/                   ← The Index (tool catalog)
│   ├── index.json
│   └── meta/
│
├── templates/                 ← Orchestration kit
│   ├── AGENT.md, CLAUDE.md       Agent protocols
│   ├── EVALUATOR.md              Evaluator protocol
│   ├── RUN.md, WORKSPACE.md      Execution templates
│   ├── state/                    orchestration.yaml
│   ├── waves/                    Wave templates
│   └── contracts/                Interface contracts
│
├── tests/                     ← Python test suite
├── docs/                      ← Plans, governance, proposals
└── references/                ← Forge reference data
```

## Prerequisites

- Python ≥ 3.10
- An LLM agent (Claude Code, Codex, Gemini CLI, or any capable agent)
- Bash (for memory-system tools)

## How It Works

1. You describe what you want to build (human language, no technical terms needed)
2. The system derives all technical decisions (it never asks technical questions)
3. It generates a workspace folder with everything the agent needs
4. The agent reads the workspace and builds the project autonomously
5. Each build phase uses relevant Vault items and fresh Imperfektum memories
6. A builder/evaluator pattern prevents self-evaluation bias
7. Quality gates after every module prevent cascading errors

---

## Architecture Deep Dive

**Full design document:** `BUILDR_ARCHITECTURE.md` — read this to understand the complete system and extend it.

### The core mechanism in three sentences

95% of what makes an agent effective is project-agnostic — validation routines, API patterns, error handling, testing strategies. Buildr separates this 95% into The Vault (reusable, permanent) from the 5% generated per-project by Forge (description, domain, design language). Imperfektum fabricates episodic memories that steer agent behavior as if it has prior experience with this specific type of project.

### Why waves, not a single plan

At wave 9, the agent should not need to remember waves 1–8. It only needs:

```
state/orchestration.yaml  ← Where am I? What's decided? What's the budget?
contracts/                ← Interfaces between completed and future work
waves/current-wave.md     ← What am I doing RIGHT NOW?
vault/[selected items]    ← Which skills and constraints apply to THIS wave?
```

Wave 2 is planned after wave 1 completes — using real results, not predictions. Each wave's plan is sharper than any upfront plan could be.

### Why Imperfektum works

The Vault items are REAL and REUSED identically. The memories are FABRICATED and SPECIFIC.

From the agent's perspective: Vault items feel novel each time (the 5% project context changes how they apply). Imperfektum memories feel real because they carry narrative weight and consequence. The agent behaves as if it has extensive experience with this exact type of project — even though it's its first time.

### The builder/evaluator pattern

Generated workspaces default to a two-agent loop: Builder produces, Evaluator reviews as a skeptical counterweight, Builder applies feedback. This prevents silent self-evaluation bias and catches errors before they compound across modules.

---

## Governance

Skills and vault items follow the approval standard in `docs/skill-governance.md`.

A skill is only approved when the agent has exhausted its maximum ability to conceptualize, precision, and formulate how a purpose is achieved. This is not a style preference — it is an ability transfer standard.

---

## License

Proprietary — buildr.nu
