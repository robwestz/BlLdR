# Buildr Memory System

Runtime memory for Buildr agents. Tracks discoveries, manages context
tiers, and enables the Imperfektum feedback loop.

## Quick Start

```bash
cd memory-system

# Start a wave (mines git, starts tracking, loads context)
./tools/wave-start.sh

# Log a discovery during work
./tools/discovery-write.sh --session wave-1 --engine claude \
  --topic form-validation --direction executing \
  --content "Blur validation must precede submit validation"

# End a wave (handoff, distill, inject, checkpoint)
./tools/wave-end.sh --session wave-1 --summary "Built booking calendar"
```

Use `--direction planning|executing|reviewing|debugging` to classify when a discovery was captured.

## Tools

| Tool | Purpose |
| ---- | ------- |
| `wave-start.sh` | One-command wave start |
| `wave-end.sh` | One-command wave end |
| `discovery-write.sh` | Log a discovery (with secret guard) |
| `discovery-distill.sh` | Compress discoveries per topic |
| `discovery-mine.sh` | Mine git commits (0 LLM tokens) |
| `context-load.sh` | Tiered context loading (hot/warm/cold) |
| `memory-inject.sh` | Inject discoveries into MEMORY.md |
| `wave-brief.sh` | Generate hot-tier brief |
| `wave-handoff.sh` | Create wave handoff contract |
| `wave-track.sh` | Track wave lifecycle |
| `checkpoint.sh` | Snapshot state to checkpoints |
| `doctor.sh` | Health check |

## The Feedback Loop

```text
Wave N starts
  → Agent reads MEMORY.md (fabricated + accumulated memories)
  → Agent builds module
  → discovery-write.sh logs what worked and what didn't
  → wave-end.sh distills discoveries
  → memory-inject.sh updates MEMORY.md with real discoveries
Wave N+1 starts
  → MEMORY.md now contains REAL memories from Wave N
  → Mixed with fabricated Imperfektum memories
  → Agent behavior improves
```

After 5 waves, MEMORY.md is majority real experience.
After 5 projects, vault/memories/ are calibrated from actual builds.
