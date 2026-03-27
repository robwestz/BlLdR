# Buildr Smith — Architecture Reference

> For the complete system architecture, see `BUILDR_ARCHITECTURE.md` at repo root.
> This file covers only Smith-specific architectural decisions.

## Smith's Place in the System

The Smith builds the **tools that other skills use**. Every vault item —
skills, constraints, strategies, routines, memories, agent templates —
is created or maintained by the Smith.

```
Smith → Vault → Operator (selects items) → Workspace → Executor (uses items)
```

## The Vault Structure

```
vault/
├── INDEX.md           ← Complete inventory (Smith maintains this)
├── skills/            ← HOW to do things (33+ items, max 60 lines each)
├── constraints/       ← WHAT NOT to do (16+ items, max 40 lines each)
├── strategies/        ← HOW TO THINK (12+ items, max 50 lines each)
├── routines/          ← VERIFICATION procedures (13+ items, max 30 lines each)
├── memories/          ← Imperfektum templates (16+ items, max 40 lines each)
│   ├── universal-*    ← All projects
│   ├── category/      ← Per project type
│   └── stack/         ← Per technology
└── agents/            ← Agent role templates (4 templates)
    ├── orchestrator.md
    ├── lead.md
    ├── specialist.md
    └── reviewer.md
```

## Key Properties

1. **Every vault item is AGNOSTIC** — works for any project type
2. **Every vault item is SELF-CONTAINED** — no references to other vault items
3. **Agent templates use {{placeholders}}** — Forge fills them per project
4. **The vault is an armory, not a library** — only relevant items are loaded per wave

## Quality Gate for Vault Items

Every item must pass:
- Under line limit for its type
- Passes agnosticism test (usable for any project type)
- Self-contained (no references to other vault items)
- Has verification/checklist component
- Uses correct template structure
- Named in kebab-case
