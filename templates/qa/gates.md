# Quality Gates — 3-Phase Validation

> Every project passes through three quality gates.
> No gate can be skipped. Each gate has binary pass/fail criteria.

---

## Gate 1: CONCEPT (Pre-Build)
**When:** After architecture decisions, before any code is written.
**Who reviews:** qa-lead (or evaluator agent)

### Checklist
- [ ] Requirements are complete and unambiguous
- [ ] Technical decisions are justified with rationale
- [ ] Module boundaries are defined with interfaces
- [ ] Risks are identified with mitigations
- [ ] A specialist can implement this without asking questions
- [ ] Design system is complete (colors, typography, spacing)
- [ ] Wave 001 scope is achievable within LOC budget

### If FAIL
Do not proceed to implementation. Fix the gaps, re-review.

---

## Gate 2: IMPLEMENTATION (Per-Wave)
**When:** After each wave completes, before marking wave as "complete".
**Who reviews:** qa-lead (or evaluator agent)

### Checklist
- [ ] All wave exit criteria met (from wave file)
- [ ] No console errors or warnings in production build
- [ ] Error states handled (not just happy path)
- [ ] Code follows SYSTEM.md standards
- [ ] No hardcoded values, no placeholder content
- [ ] No files exceed 300 lines
- [ ] Responsive at 320px, 768px, 1024px (UI projects)
- [ ] Contract interfaces match between modules
- [ ] All new files have clear purpose (no orphans)

### If FAIL
Fix issues in current wave. Do not proceed to next wave.

---

## Gate 3: DELIVERY (Final)
**When:** After all waves complete, before declaring project done.
**Who reviews:** qa-lead (or evaluator agent) + human

### Checklist
- [ ] All modules integrated and working end-to-end
- [ ] All acceptance criteria from PROJECT.md met
- [ ] Lighthouse score >= 90 (UI projects)
- [ ] WCAG AA compliance verified (UI projects)
- [ ] All API endpoints return correct status codes (API projects)
- [ ] No known bugs (or all documented with severity)
- [ ] Documentation complete (README, deployment guide)
- [ ] Production build succeeds without errors
- [ ] State/orchestration.yaml shows all waves complete

### If FAIL
Create fix wave. Address issues. Re-run Gate 3.

---

## Severity Classification

When a gate check fails, classify each issue:

| Severity | Meaning | Action |
|----------|---------|--------|
| **BLOCKER** | Cannot ship. Breaks core functionality or security. | Fix before proceeding |
| **SHOULD_FIX** | Degrades quality. Not broken but not acceptable. | Fix in current wave |
| **NITPICK** | Minor. Style, naming, non-functional. | Fix if time allows |

Gate passes only when zero BLOCKER issues remain.
