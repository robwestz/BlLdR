# Skill Governance Standard

**The approval gate for every Buildr skill, vault item, and system artifact.**

---

## The Principle

A skill is only approved when the agent has exhausted its maximum ability to:
1. **Conceptualize** the purpose it serves
2. **Precision** — every ambiguity resolved, every edge case addressed
3. **Formulate** — no sentence could be sharper, no step more exact

A skill is **not** approved when the agent could still produce a more precise, more complete, or more purposeful formulation. Being "good enough" is never the bar. A skill is approved when *nothing more can be won through better formulation, clearer structure, deeper conceptualization, or higher linguistic precision*.

This is not a linguistic exercise — it is an ability transfer. The skill must carry the agent's full competence for the purpose. A convenient packaging of something an agent could still express better in ordinary instruction is not a skill. It is bureaucracy.

---

## Classification Decision Tree

Before creating any system artifact, classify it:

```
Is it instructions for HOW to perform a specific task?
  YES → Vault Skill (vault/skills/)
  NO ↓

Is it a prohibition — what NOT to do?
  YES → Vault Constraint (vault/constraints/)
  NO ↓

Is it a thinking pattern for making decisions?
  YES → Vault Strategy (vault/strategies/)
  NO ↓

Is it a repeatable verification procedure?
  YES → Vault Routine (vault/routines/)
  NO ↓

Is it a behavioral nudge — a fabricated experience to steer agent defaults?
  YES → Memory Template (vault/memories/)
  NO ↓

Is it a system-level pipeline for orchestrating the Buildr system itself?
  YES → System Skill (skills/[name]/SKILL.md)
  NO ↓

Is it reference material — immutable domain knowledge?
  YES → Reference document (references/ or skills/[name]/references/)
  NO →  You don't need to create an artifact. Write instructions directly.
```

---

## Approval Criteria by Type

### Vault Skills
A vault skill is approved when:
- [ ] Every step is a concrete verb phrase — no abstract direction
- [ ] Verification is binary (pass/fail, not "looks right")
- [ ] Common Mistakes section catches the top 2-5 failure modes with exact alternatives
- [ ] Passes the four-project agnosticism test (booking / SaaS / CLI / e-commerce)
- [ ] Under 60 lines — if more is needed, the scope is wrong
- [ ] An agent could follow it to completion without reading any other file

### Vault Constraints
Approved when:
- [ ] Each prohibition has exactly three parts: Banned → Why (consequence) → Instead (alternative)
- [ ] "Why" is a consequence, not a philosophy ("causes 23-file rework", not "is bad practice")
- [ ] "Instead" is a concrete action
- [ ] Under 40 lines
- [ ] Agnosticism test passes

### Vault Strategies
Approved when:
- [ ] Contains at least one explicit IF/THEN decision point
- [ ] "Traps" section catches the two most common wrong turns
- [ ] Under 50 lines
- [ ] No sentence is purely theoretical — every sentence helps make a decision

### Vault Routines
Approved when:
- [ ] Every check is binary — no subjective items
- [ ] "If fails" section is present and actionable
- [ ] Includes expected duration
- [ ] Under 30 lines

### Memory Templates
Approved when:
- [ ] Scars have specific consequences (numbers, time, files affected — never vague)
- [ ] "Now we" phrases are imperatives, not principles
- [ ] Past tense throughout (this is memory, not instruction)
- [ ] Self-contained — no references to other vault items

### System Skills (skills/)
These carry the highest bar. Approved when:
- [ ] The pipeline is exhaustive — no phase can be added that would improve outcomes
- [ ] Every quality gate is explicit and binary
- [ ] Triggers (when to use) are unambiguous — no overlap with other system skills
- [ ] Agent can execute the entire pipeline without human intervention for the nominal case
- [ ] Edge cases are explicitly named, not implied
- [ ] Self-contained with its own references/ folder if domain knowledge is needed

---

## The Final Test

Before approving any artifact, the author must be able to say:

> *"I cannot produce a more precise, more complete, or more purposeful version of this. Every word earns its place. Every step is necessary and sufficient. An agent using this will perform at the level I would perform if I had full attention and expertise on this task."*

If any doubt exists — rewrite.

---

## Anti-Patterns

### ❌ The Comfortable Package
Writing a skill because it feels tidy to have one, when the content could be expressed better as a direct instruction in the agent's context.

### ❌ The Theory Article
A skill that explains why something matters but doesn't tell an agent what to do next.

### ❌ The Infinite Scope
A skill that tries to cover a domain instead of a task. "API Development" is a domain. "Design and implement a single REST endpoint" is a task.

### ❌ The Subjective Checklist
A routine with items like "looks responsive" or "seems accessible." Every check must be objectively verifiable.

### ❌ The Stale Memory
A memory template with consequences like "things got messy" — not specific enough to steer behavior. Needs numbers, time, file counts, client reactions.

---

## Vault Gap Identification

Run this analysis before any authoring session:

```
Vault targets (from buildr-smith/SKILL.md):
  Skills:     16 current / 30-40 target → need 14-24
  Constraints: 10 current / 15-20 target → need 5-10
  Strategies:   8 current / 10-15 target → need 2-7
  Routines:     6 current / 10-15 target → need 4-9
  Memories:    12 current / 20-30 target → need 8-18
```

When identifying gaps, ask: *"What do agents currently handle inconsistently or badly that a vault item would prevent?"* — not *"What topic isn't covered?"*

Coverage of a topic is not a gap. Prevention of a failure mode is.
