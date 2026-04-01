# Preflight Retention Policy

Rules for git, retention, and immutability of preflight staging artifacts under `v2/.buildr/preflight/<project-slug>/`.

---

## Git Default

`v2/.buildr/` is listed in the root `.gitignore`. Preflight artifacts are runtime staging and are not committed by default.

### Exception: Audit Evidence

Teams that require reproducible evidence of preflight decisions may commit specific files. To do this, add negation rules to `.gitignore`:

```gitignore
v2/.buildr/
!v2/.buildr/preflight/*/PREFLIGHT_APPROVAL.json
!v2/.buildr/preflight/*/PREFLIGHT_DECISIONS.json
!v2/.buildr/preflight/*/PREFLIGHT_ACCEPTANCE.json
```

This is a team-level decision. The system default is gitignored.

---

## Retention Rules

### Reruns (same slug, non-approved artifacts)

If `v2/.buildr/preflight/<slug>/` exists and does NOT contain `PREFLIGHT_APPROVAL.json` with `status: approved`: **overwrite** all artifacts. The previous run was abandoned or incomplete.

### Reruns (same slug, approved artifacts)

If `v2/.buildr/preflight/<slug>/` exists and contains `PREFLIGHT_APPROVAL.json` with `status: approved`: **create a new directory** with a timestamp suffix:

```
v2/.buildr/preflight/<slug>-YYYYMMDDTHHMMSS/
```

The original approved artifacts are preserved.

### Abandoned runs

Artifacts from abandoned or rejected runs are cleaned up on the next run for the same slug (overwrite rule). There is no automatic cleanup of abandoned artifacts across different slugs.

---

## Immutability

### After `status: approved`

All artifacts in the staging directory are **immutable**. They may not be modified by any process unless preflight is explicitly reopened.

Manual edits to approved artifacts are forbidden. They break the chain of trust between preflight analysis and workspace generation.

### Reopening preflight

Requires explicit user action. Creates a new run (new timestamped slug if collision). The previous approved artifacts are preserved. Reopening is a full pipeline rerun from Phase 1 — individual phases cannot be selectively rerun.

### After `status: rejected` or `status: insufficient_information`

Artifacts are mutable. They will be overwritten on the next run for the same slug.

---

## Interaction with Production-Grade Expectations

Preflight artifacts serve two purposes:

1. **Runtime gate:** `PREFLIGHT_APPROVAL.json` gates workspace generation. This is ephemeral — it needs to exist during the generation session.
2. **Decision evidence:** `PREFLIGHT_DECISIONS.json` and `PREFLIGHT_ACCEPTANCE.json` record why the architecture was approved. This has long-term value for audits, disputes, and retrospectives.

For production-grade use, commit the evidence files (see Exception above). For development/experimentation, the gitignore default is sufficient.
