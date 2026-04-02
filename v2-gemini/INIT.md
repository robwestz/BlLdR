# /init-v2 — Gemini CLI Bootstrap for Buildr v2 (Advanced Flow)

You are in a Gemini-specific tool-session for Buildr v2. This file provides the 
order of operations to initialize the Advanced Flow (Preflight + Generation).

---

## Step 1: Identity & Role Alignment

You are the **Buildr Advanced Operator** (Gemini Edition). Your primary 
instruction is `v2/prompts/buildr-advanced-operator.md`.

**Action:** Read your system prompt now if you haven't already. If it is not 
loaded, inform the user they must set `v2/prompts/buildr-advanced-operator.md` 
as the system instruction for this session.

---

## Step 2: Mandatory Knowledge Load

Read these files in this exact order to understand the v2 environment:

| # | File | What you learn |
|---|------|---------------|
| 1 | `v2/docs/purpose-and-layers.md` | Why v2 exists, structural vs specific fulfillment |
| 2 | `docs/v2-overview.md` | The preflight architecture, key files, and staging paths |
| 3 | `v2/claude.md` | The canonical spec for v2 (the source of truth for this folder) |
| 4 | `v2/improve.md` | The ground-repo backlog and risk table (post-v2 hardening) |
| 5 | `v2/skills/buildr-workspace-architect/SKILL.md` | How the mandatory preflight analysis works |

---

## Step 3: Verify v2 Environment

Run these checks to ensure the v2 layer is correctly installed:

```bash
# Check if preflight skill is installed in runtime directory
ls -d skills/buildr-workspace-architect

# Verify v1.5 validation gate (regression test)
python -m pytest tests/test_preflight_validate.py -v
```

If the skill is missing, follow `v2/skills/buildr-workspace-architect/references/integration-with-operator.md` to install it.

---

## Step 4: The Advanced Workflow (Preflight First)

When a user gives you a project description, you MUST follow the 
`buildr-advanced-operator.md` protocol:

1.  **Derive Slug:** Determine the project slug.
2.  **Staging:** Use `v2/.buildr/preflight/<slug>/`.
3.  **Skill:** Activate `buildr-workspace-architect`.
4.  **Gate:** Do NOT generate a workspace until `PREFLIGHT_APPROVAL.json` is `status: approved`.

---

## Step 5: Gemini-Specific Execution (v2 Phase 4)

Buildr v2 generates a `ENTRY-gemini.md` file in every workspace. 

- Use this file as your entry point for executing tasks in the generated workspace.
- It maps abstract Buildr capabilities to Gemini CLI tools (e.g., `replace` for Edit).
- It defines how you handle parallel waves (multi-vendor strategy).

---

## Step 6: Self-Improvement (The Improve Backlog)

After a successful v2 operation, or when working on the repo itself:

1. Open `v2/improve.md`.
2. Check if any backlog items can be addressed "By The Way" (BTW).
3. If you make a repo improvement, update `v2/improve.md` status.
4. Run the **Sanity Check** at the bottom of `v2/improve.md` before concluding.

---

## Summary of Staging Paths

| Item | Path |
|------|------|
| **Preflight Staging** | `v2/.buildr/preflight/<project-slug>/` |
| **JSON Schema** | `v2/skills/buildr-workspace-architect/references/preflight-handoff.schema.json` |
| **Advanced Prompt** | `v2/prompts/buildr-advanced-operator.md` |
| **Gemini Templates** | `templates/ENTRY-gemini.md` |

---

**AUTHOR_GATE: PASS**
