# Entry Point — Claude Code

> Read this file to start building this project with Claude Code (Anthropic).

## Quick Start

1. Read `CLAUDE.md` — orchestration protocol, roles, quality gates
2. Read `agents/agent-manifest.json` — your team roster
3. Follow `RUN.md` — the canonical execution loop

## Model Tier Mapping

| Role | Model | When to Use |
|------|-------|-------------|
| Orchestrator | opus | Architecture decisions, delegation, conflict resolution |
| Lead | opus | Domain architecture, spec review, cross-module coordination |
| Specialist (builder) | sonnet | Implementation, file creation, component building |
| Specialist (test) | sonnet | Test writing, QA execution |
| Reviewer (qa-lead) | sonnet | Code review, acceptance verification |
| Deploy | haiku | Build scripts, config files, CI/CD |

## Tool Mapping

| Abstract Capability | Claude Code Tool |
|---------------------|-----------------|
| file_read | Read |
| file_write | Write, Edit |
| file_search | Glob, Grep |
| bash_execute | Bash |
| web_fetch | WebFetch |
| spawn_agent | Agent (subagent_type, model parameter) |

## Spawning Sub-Agents

The orchestrator delegates to specialists using the Agent tool:

```
Agent(
  prompt="Implement the DatePicker component per modules/04-booking-calendar.md spec",
  model="sonnet",
  name="ui-builder"
)
```

For parallel waves (see `parallel_phases` in `state/orchestration.yaml`):
- Spawn one Agent per independent wave
- Each agent gets: wave file + module spec + relevant contracts
- Wait for all to complete before proceeding to next phase

## Evaluator Invocation

After each wave, spawn the evaluator:

```
Agent(
  prompt="Review wave 004-booking-calendar. Read EVALUATOR.md for format. Write to qa/evaluations/004-booking-calendar.md",
  model="sonnet",
  name="qa-lead"
)
```
