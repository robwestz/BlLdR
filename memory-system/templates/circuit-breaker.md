# Circuit Breaker Log

## Rules
Any agent increments `Attempts` each time a task is sent BACK for rework.
**Attempts >= 3** → Status becomes `BLOCKED_HUMAN` → SYSTEM STOPS.
Human must intervene before work resumes.

## Active Issues

| Task ID | Agent | Attempts | Latest Error |
|---------|-------|----------|-------------|
| — | — | 0 | System initialized |

## Resolved
<!-- Move resolved issues here with resolution notes -->
