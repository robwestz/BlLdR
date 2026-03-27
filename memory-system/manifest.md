# Memory System Tools Manifest

| Tool | Input | Output |
|------|-------|--------|
| `discovery-write.sh` | `--session --engine --topic --content [--type --direction --artifacts]` | JSON line in discoveries.jsonl |
| `context-load.sh` | `[--tier hot/warm/cold] [--budget N] [--refresh]` | stdout (markdown) |
| `memory-inject.sh` | discoveries.jsonl + MEMORY.md with markers | Updated MEMORY.md |
| `wave-brief.sh` | discoveries.jsonl + PROJECT.md | context/wave-brief.md |
| `discovery-distill.sh` | discoveries.jsonl | context/distilled.md |
| `wave-handoff.sh` | `--session S --summary "..."` | context/handoff.md |
| `discovery-mine.sh` | git log | JSON lines in discoveries.jsonl |
| `wave-track.sh` | `--start / --end / --list` | Session JSON in continuum/sessions/ |
| `checkpoint.sh` | `[--slug NAME] [--auto]` | Checkpoint dir with manifest |
| `wave-start.sh` | `[--tier T] [--engine E]` | Context to stdout |
| `wave-end.sh` | `--session S --summary "..."` | All artifacts updated |
| `doctor.sh` | `[--verbose]` | OK / issues with fixes |

## Rules

- Every tool does ONE job
- `set -euo pipefail` in all scripts
- All tools are chmod +x
- JSON schema fields are NEVER renamed
- Portability: Linux, macOS, Windows (Git Bash)
