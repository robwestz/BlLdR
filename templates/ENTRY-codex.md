# Entry Point — OpenAI Codex / ChatGPT

> Read this file to start building this project with OpenAI Codex CLI or ChatGPT.

## Quick Start

1. Read `CLAUDE.md` — orchestration protocol (vendor-agnostic despite the name)
2. Read `agents/agent-manifest.json` — your team roster
3. Follow `RUN.md` — the canonical execution loop

## Model Tier Mapping

| Role | Model | When to Use |
|------|-------|-------------|
| Orchestrator | o3 / o4-mini-high | Architecture decisions, delegation, conflict resolution |
| Lead | o3 / o4-mini-high | Domain architecture, spec review |
| Specialist (builder) | o4-mini | Implementation, file creation, component building |
| Specialist (test) | o4-mini | Test writing, QA execution |
| Reviewer (qa-lead) | o4-mini | Code review, acceptance verification |
| Deploy | o4-mini | Build scripts, config files |

## Tool Mapping

| Abstract Capability | Codex Tool |
|---------------------|-----------|
| file_read | read_file, shell (cat) |
| file_write | write_file, apply_diff |
| file_search | shell (find, grep) |
| bash_execute | shell |
| web_fetch | shell (curl) |
| spawn_agent | Not built-in — use sequential execution per wave |

## Execution Without Sub-Agents

Codex CLI does not natively spawn sub-agents. Instead:

1. Execute waves sequentially (follow `state/orchestration.yaml` wave order)
2. For parallel phases: run separate Codex sessions in different terminals, one per wave
3. Each session reads: the wave file + module spec + contracts
4. After each wave: manually run evaluator review (or use a separate Codex session)

## Evaluator Invocation

After completing a wave, start a new prompt:

```
Read EVALUATOR.md. Review the code changes for wave 004-booking-calendar.
Write structured feedback to qa/evaluations/004-booking-calendar.md.
Follow the YAML front-matter format specified in EVALUATOR.md.
```
