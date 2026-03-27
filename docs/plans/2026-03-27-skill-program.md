# Skill Program — Session Backlog

**Created:** 2026-03-27
**Standard:** Every item must pass `docs/skill-governance.md` before approval.
**Priority:** H = High (prevents known failure modes), M = Medium (expands capability), L = Low (coverage)

---

## Session Status

### Completed this session (2026-03-27)
- [x] `docs/skill-governance.md` — approval standard and classification guide
- [x] `vault/skills/research.md` — systematic topic research
- [x] `vault/skills/code-review.md` — code quality review
- [x] `vault/skills/component-arch.md` — UI component architecture
- [x] `vault/skills/data-fetch.md` — remote data fetch, cache, display
- [x] `skills/buildr-executor/SKILL.md` — executing a Buildr workspace end-to-end
- [x] `vault/skills/error-boundary.md` — React error boundaries, fallback, recovery
- [x] `vault/skills/environment-config.md` — env vars, secrets, fail-fast validation
- [x] `vault/skills/database-schema.md` — schema naming, FKs, migrations, indexes
- [x] `vault/skills/input-sanitization.md` — server-side sanitization, parameterized queries
- [x] `vault/skills/realtime-updates.md` — WebSocket/SSE/polling decision + wiring
- [x] `vault/skills/file-upload.md` — upload flow, magic-byte validation, storage
- [x] `vault/skills/pagination.md` — offset vs cursor, URL state, empty page
- [x] `vault/skills/search-filter.md` — debounce, client/server threshold, URL filters
- [x] `vault/skills/notification-system.md` — type-based timing, stacking, aria-live
- [x] `vault/skills/modal-dialog.md` — focus trap, Escape, scroll lock, return focus
- [x] `vault/skills/drag-drop.md` — visual feedback, keyboard, touch, persistence
- [x] `vault/skills/dark-mode.md` — CSS vars, flash-free init, localStorage
- [x] `vault/constraints/no-untyped-props.md`
- [x] `vault/constraints/no-direct-db-in-ui.md`
- [x] `vault/constraints/no-magic-routes.md`
- [x] `vault/constraints/no-sync-in-async.md`
- [x] `vault/constraints/no-implicit-any.md`
- [x] `vault/strategies/tech-choice.md`
- [x] `vault/strategies/when-to-cache.md`
- [x] `vault/strategies/error-vs-feature.md`
- [x] `vault/strategies/test-scope.md`
- [x] `vault/routines/pre-commit.md`
- [x] `vault/routines/security-check.md`
- [x] `vault/routines/performance-check.md`
- [x] `vault/routines/dependency-audit.md`
- [x] `vault/memories/stack/typescript-memories.md`
- [x] `vault/memories/stack/prisma-memories.md`
- [x] `vault/memories/category/api-memories.md`
- [x] `vault/memories/category/dashboard-memories.md`

---

## Next Session — Vault Skills (gap: 0-8 remaining toward 30-40 target)

| Priority | File | Purpose |
|----------|------|---------|
| L | `vault/skills/print-layout.md` | Print CSS, page breaks, print-specific content |

---

## Next Session — Vault Constraints (gap: 0-5 toward 15-20 target)

All H/M-priority constraints completed. Remaining are optional expansions.

---

## Next Session — Vault Strategies (gap: 0-3 toward 10-15 target)

All H/M-priority strategies completed. Remaining are optional expansions.

---

## Next Session — Vault Routines (gap: 0-5 toward 10-15 target)

All H/M-priority routines completed. Remaining are optional expansions.

---

## Next Session — Memory Templates (gap: 4-14 toward 20-30 target)

| Priority | File | Scope |
|----------|------|-------|
| M | `vault/memories/category/mobile-memories.md` | React Native / mobile-first projects |
| L | `vault/memories/stack/tailwind-memories.md` | Tailwind CSS patterns |
| L | `vault/memories/category/realtime-memories.md` | Real-time / live-update apps |

---

## Next Session — System Skills

| Priority | Skill | Purpose |
|----------|-------|---------|
| H | `skills/buildr-auditor/SKILL.md` | Audits an existing Vault for gaps, drift, redundancy |
| M | `skills/buildr-retrospective/SKILL.md` | Conducts post-wave retrospective, updates memory + log |
| M | `skills/buildr-scaffolder/SKILL.md` | Generates module scaffold from wave spec (code-level) |

---

## Execution Instructions for Next Session

1. Read `docs/skill-governance.md` in full before creating any item
2. Run agnosticism test on every vault item before writing
3. Write items in priority order within each type
4. After every 5 items: spot-check two random existing vault items for drift
5. Update `vault/INDEX.md` after each batch (never at the end — minimize loss on interruption)
6. Run `python -m unittest -v` after any engine changes triggered by gaps discovered
7. End session: update this file to reflect what was completed

---

## Progress Tracking

```
Vault snapshot (before this session):
  Skills:      16 / 30-40  (53% of minimum)
  Constraints: 10 / 15-20  (67% of minimum)
  Strategies:   8 / 10-15  (80% of minimum)
  Routines:     6 / 10-15  (60% of minimum)
  Memories:    12 / 20-30  (60% of minimum)
  Total:       52 / 85-120 (61% of minimum)

After this session (+16 vault skills, +5 constraints, +4 strategies, +4 routines, +4 memories, +1 system skill):
  Skills:      32 / 30-40  (107% of minimum ✓ TARGET MET)
  Constraints: 15 / 15-20  (100% of minimum ✓ TARGET MET)
  Strategies:  12 / 10-15  (120% of minimum ✓ TARGET MET)
  Routines:    10 / 10-15  (100% of minimum ✓ TARGET MET)
  Memories:    16 / 20-30   (80% of minimum — 4 remaining)
  Total:       85 / 85-120 (100% of minimum ✓)
```
