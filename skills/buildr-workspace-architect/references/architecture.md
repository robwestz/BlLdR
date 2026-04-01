# Architecture Reference — Buildr Workspace Architect

## Where This Skill Sits in Buildr

```
Human project description
    |
    v
[buildr-workspace-architect]   <-- THIS SKILL (preflight)
    |
    v  (approved preflight artifacts)
    |
[operator-like generation]     <-- Existing operator pipeline (Phases 2-5)
    |
    v  (generated workspace)
    |
[buildr-executor]              <-- Separate skill, unchanged
    |
    v  (completed project)
```

The workspace-architect sits between the human's request and workspace generation. It is the mandatory gate that prevents unexamined assumptions from flowing into the workspace.

---

## Why This Is a System Skill

The governance classification tree (`docs/skill-governance.md`) asks: "Is it a system-level pipeline for orchestrating the Buildr system itself?" This skill answers yes on every axis:

1. **It orchestrates the system.** It gates a critical system boundary (workspace generation), not a task within a project.
2. **It requires a multi-phase pipeline.** Five sequential phases with inter-phase dependencies, binary gates, and structured artifacts exceed what a vault item can express (vault skills are max 60 lines, single-purpose, self-contained).
3. **It has its own reference domain.** Approval semantics, handoff contracts, phase anti-patterns, and operator integration require a dedicated `references/` folder.
4. **Removing it causes material regression.** Without this skill, workspace generation proceeds from unexamined assumptions. The preflight gate is not decorative — it is structural.

### System Skills vs. Vault Items

| Dimension | Vault Skill | System Skill (this) |
|-----------|------------|---------------------|
| Scope | Single task | Multi-phase pipeline |
| Size | Max 60 lines | Unlimited (complexity-justified) |
| Dependencies | Self-contained | Inter-phase + cross-skill |
| Governance | Agnosticism test | Exhaustive pipeline test |
| Output | Agent behavior change | Structured artifacts + gate |
| Reference material | None (self-contained) | Own `references/` folder |

---

## Why This Is Not a Vault Item

A vault item must pass the four-project agnosticism test (booking / SaaS / CLI / e-commerce) and be self-contained in under 60 lines. This skill:

- Has five sequential phases with binary gates between them.
- Produces 15+ structured artifacts.
- Requires inter-phase state (Phase 3 reads Phase 1 + 2 outputs).
- Defines a machine-readable schema for handoff contracts.
- Gates another system skill (operator-like generation).

No vault item format can contain this. Forcing it into a vault item would require either collapsing the phases (losing the gating mechanism) or splitting into five vault items (losing the pipeline coherence). Both options degrade the outcome.

---

## Why This Is Not Just an Agent-Prompt Section

An agent-prompt section (like adding a "think before you build" paragraph to the operator prompt) would:

- Be advisory, not mandatory — the agent could skip it under time pressure or ambiguous instructions.
- Lack structured artifacts — reasoning would be freeform text, not machine-readable payloads.
- Lack binary gates — there would be no clear pass/fail boundary.
- Collapse under context pressure — long prompts get summarized or ignored in late-context positions.
- Be impossible to validate programmatically in future v2+ code enforcement.

The skill format makes preflight a first-class operation with its own trigger, inputs, outputs, gates, and failure states. This is materially different from a prompt paragraph.

---

## Why This Is Not Executor Logic

The executor (`buildr-executor`) picks up a generated workspace and builds it wave by wave. Its state machine starts at `WORKSPACE_READY`. It reads `AGENT.md`, `RUN.md`, and `state/orchestration.yaml`.

Preflight operates before any workspace exists. It takes a human description, not a workspace. It produces architectural analysis, not code. It gates generation, not execution.

| Dimension | Workspace Architect | Executor |
|-----------|-------------------|----------|
| Input | Human description | Generated workspace |
| Output | Preflight artifacts + approval | Completed project (code, tests) |
| Timing | Before workspace exists | After workspace is generated |
| Decision-making | High — defines architecture | Low — follows pre-made decisions |
| State machine | None (pipeline) | WORKSPACE_READY -> COMPLETE |

Merging preflight into the executor would conflate two fundamentally different concerns: deciding what to build vs. building it. The executor's value is that it does not question architecture — it executes it faithfully. Burdening it with architectural analysis would weaken both functions.

---

## Why This Is Not a Replacement for Operator

The existing `buildr-operator` skill takes a human description through five phases: Onboarding, Derive, Select, Generate, Verify. This skill does not replace that pipeline.

Instead, this skill inserts a mandatory preflight stage before the operator pipeline begins. After preflight approval, operator-like generation (Phases 2-5 of the existing operator) runs with the additional constraint that it cannot contradict approved preflight.

The operator's core strength — deriving technical decisions, selecting vault items, generating workspace structure — is preserved. What changes is that the operator now operates within bounds set by preflight rather than from unbounded inference.

| Without Preflight | With Preflight |
|-------------------|----------------|
| Description -> Derive -> Select -> Generate | Description -> **Preflight** -> Derive -> Select -> Generate |
| Operator infers everything from description | Operator infers within preflight-approved bounds |
| No structured gate before generation | Binary gate: approved/rejected/insufficient |
| Assumptions flow unchecked into workspace | Assumptions are surfaced, challenged, and recorded |

---

## Why One Advanced Agent + One Preflight Skill Is the Right First Implementation

The simplest correct implementation is:

1. **One advanced agent identity** (`buildr-advanced-operator.md`) that orchestrates the flow.
2. **One preflight skill** (`buildr-workspace-architect/SKILL.md`) that runs the pipeline.

This is the right first step because:

- **Minimal surface area.** One prompt + one skill. No new engines, no new runtime infrastructure.
- **v1 prompt-enforced.** The agent follows the prompt. No code changes required in forge/bridge.
- **Clear upgrade path.** v2+ adds schema validation in forge/bridge without changing the skill or prompt.
- **No premature decomposition.** Splitting preflight into five separate skills (one per phase) would create coordination overhead without adding value — the phases are sequential and tightly coupled.
- **No premature automation.** The pipeline is agent-driven, not code-driven. This lets us refine the phases through usage before committing to code.

---

## How This Avoids the "Comfortable Package" Anti-Pattern

The governance standard defines the "Comfortable Package" anti-pattern as: "Writing a skill because it feels tidy to have one, when the content could be expressed better as a direct instruction in the agent's context."

This skill avoids that anti-pattern because:

1. **The content cannot be expressed as a direct instruction.** Five gated phases with 15+ artifacts, binary gates, inter-phase dependencies, and a machine-readable schema exceed what a prompt paragraph can contain or enforce.
2. **Removing this skill degrades outcomes.** Without structured preflight, workspace generation proceeds from unexamined assumptions — a measurable quality regression, not a tidiness loss.
3. **The skill has its own domain knowledge.** Approval semantics, ELS categories, CRI fields, decision record structure, and acceptance criteria packaging are domain-specific concepts that require reference material.
4. **The skill gates another operation.** It is not decorative — it is structural. The operator cannot proceed without its output.

If the content of this skill could be expressed as three sentences in the operator prompt and produce the same outcome, it would be a Comfortable Package. It cannot.

---

## v1 Prompt-Enforced vs. v2+ Code-Enforced

### v1 (Current)

- The advanced operator prompt instructs the agent to run preflight before generation.
- The agent writes preflight artifacts to the staging directory.
- The agent reads `PREFLIGHT_APPROVAL.json` and blocks generation if status is not `approved`.
- Compliance depends on the agent following instructions.
- A misconfigured or poorly prompted agent could bypass the gate.

### v2+ (Future)

- `forge_engine.py` adds a pre-generation hook that:
  1. Checks for `v2/.buildr/preflight/<slug>/PREFLIGHT_APPROVAL.json`.
  2. Validates the file against `preflight-handoff.schema.json`.
  3. Rejects generation if `status` is not `approved` or if the schema is invalid.
- `bridge.py` adds a validation step that:
  1. Verifies all required artifacts exist in the staging directory.
  2. Cross-references `PREFLIGHT_ACCEPTANCE.json` criteria against the generated workspace's QA checklist.
- Code enforcement makes bypass impossible regardless of agent behavior.
- The transition requires no changes to `SKILL.md` or the advanced operator prompt.

### What Changes Between v1 and v2+

| Aspect | v1 | v2+ |
|--------|----|----|
| Gate enforcement | Agent reads prompt | Code validates schema |
| Bypass risk | Possible (agent error) | Impossible (code blocks) |
| Schema validation | Agent interprets | `jsonschema` library validates |
| Cross-reference checks | Agent performs | Bridge automates |
| Skill/prompt changes | None needed | None needed |
| Engine changes | None | forge + bridge add hooks |
