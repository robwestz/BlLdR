# Entry Point — Google Gemini CLI

> Read this file to start building this project with Gemini CLI.

## Quick Start

1. Read `CLAUDE.md` — orchestration protocol (vendor-agnostic despite the name)
2. Read `agents/agent-manifest.json` — your team roster
3. Follow `RUN.md` — the canonical execution loop

## Model Tier Mapping

| Role | Model | When to Use |
|------|-------|-------------|
| Orchestrator | gemini-2.5-pro | Architecture decisions, delegation, conflict resolution |
| Lead | gemini-2.5-pro | Domain architecture, spec review |
| Specialist (builder) | gemini-2.5-flash | Implementation, file creation, component building |
| Specialist (test) | gemini-2.5-flash | Test writing, QA execution |
| Reviewer (qa-lead) | gemini-2.5-flash | Code review, acceptance verification |
| Deploy | gemini-2.5-flash | Build scripts, config files |

## Tool Mapping

| Abstract Capability | Gemini CLI Tool |
|---------------------|----------------|
| file_read | read_file, shell (cat) |
| file_write | edit_file, shell |
| file_search | shell (find, grep) |
| bash_execute | shell |
| web_fetch | shell (curl), google_web_search |
| spawn_agent | Not built-in — use sequential execution or parallel terminals |

## Execution Without Sub-Agents

Gemini CLI does not natively spawn sub-agents. Instead:

1. Execute waves sequentially (follow `state/orchestration.yaml` wave order)
2. For parallel phases: run separate Gemini sessions in different terminals, one per wave
3. Each session reads: the wave file + module spec + contracts
4. After each wave: manually run evaluator review (or use a separate session)

## Evaluator Invocation

After completing a wave, start a new prompt:

```
Read EVALUATOR.md. Review the code changes for wave 004-booking-calendar.
Write structured feedback to qa/evaluations/004-booking-calendar.md.
Follow the YAML front-matter format specified in EVALUATOR.md.
```

## Multi-Vendor Parallel Strategy

For maximum speed, combine vendors across independent waves:

```
Phase 3 (parallel):
  Terminal 1 (Claude): wave 003-booking-catalog
  Terminal 2 (Gemini): wave 007-multilingual  
  Terminal 3 (Codex):  wave 008-seo
  Terminal 4 (Claude): wave 006-whatsapp
```

Each terminal reads only its wave file + module spec + relevant contracts.
Shared state (orchestration.yaml) is updated by each after completion.
