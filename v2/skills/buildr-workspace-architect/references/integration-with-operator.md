# Integration with Operator — Buildr Workspace Architect

## How the Advanced Agent Hands Approved Preflight into Generation

After `PREFLIGHT_APPROVAL.json` has `status: approved`, the advanced operator proceeds to workspace generation using the existing operator pipeline (Phases 2-5 of `buildr-operator/SKILL.md`: Derive, Select, Generate, Verify).

### Handoff sequence

```
1. Advanced operator reads PREFLIGHT_APPROVAL.json
   -> Confirms status: approved
   -> Confirms all 15 artifacts exist

2. Advanced operator loads preflight artifacts as normative input:
   -> PREFLIGHT_PURPOSE.json    (CRI fields -> non-negotiable project constraints)
   -> PREFLIGHT_ARCHITECTURE.json (minimal-inevitable set -> normative component list)
   -> PREFLIGHT_ACCEPTANCE.json (acceptance criteria -> binding QA requirements)
   -> PREFLIGHT_DECISIONS.json  (decision records -> normative architectural decisions)
   -> PREFLIGHT_ABSENCE_MAP.json (ELS risks -> workspace_gen mitigation items)
   -> PREFLIGHT_BUILD_ORDER.md  (recommended build sequence -> wave ordering input)

3. Advanced operator invokes operator-like generation:
   -> Phase 2 (Derive): constrained by CRI, minimal-inevitable set, and decisions
   -> Phase 3 (Select): vault items selected within approved architectural scope
   -> Phase 4 (Generate): workspace produced with preflight as normative foundation
   -> Phase 5 (Verify): verification includes preflight compliance check

4. Generated workspace includes:
   -> All standard workspace files (WORKSPACE.md, PROJECT.md, etc.)
   -> qa/acceptance.md derived from PREFLIGHT_ACCEPTANCE.json
   -> Preflight artifacts referenced from workspace (not duplicated)
```

### How preflight artifacts enter the workspace

The generated workspace REFERENCES the preflight staging directory — it does not duplicate the artifacts.

In the generated workspace's `WORKSPACE.md`, add a section:

```markdown
## Preflight Reference

This workspace was generated from approved preflight:
- Staging: v2/.buildr/preflight/<project-slug>/
- Approval: PREFLIGHT_APPROVAL.json (status: approved)
- Acceptance: PREFLIGHT_ACCEPTANCE.json (binding criteria)
- Decisions: PREFLIGHT_DECISIONS.json (normative records)
```

The workspace's `qa/acceptance.md` must be derived from `PREFLIGHT_ACCEPTANCE.json`:
- Every `acceptance_id` in the preflight acceptance payload must appear as a QA item.
- No preflight acceptance criterion may be silently dropped.
- The workspace may add additional QA items beyond preflight criteria.

---

## What Operator-Like Generation May Still Decide

After preflight approval, the operator pipeline retains authority over:

| Decision Area | Example | Why Operator Decides This |
|--------------|---------|--------------------------|
| **Module decomposition** | Split "auth" into "auth-login" + "auth-registration" modules | Granularity within approved architecture is an implementation concern |
| **File structure** | `src/components/auth/LoginForm.tsx` | File naming and directory layout are implementation details |
| **Wave sequencing** | Foundation -> Auth -> Booking -> Payment | Build order within approved components (may use PREFLIGHT_BUILD_ORDER.md as input) |
| **Vault item selection** | Select `auth-patterns.md` for the auth wave | Which specific vault skills apply to which wave |
| **Imperfektum memories** | Generate booking-specific scars for wave 3 | Per-wave memory generation is operator's concern |
| **Design system** | Blue palette, Inter font, 4px spacing grid | Visual design unless constrained by CRI |
| **Implementation patterns** | REST vs. GraphQL within the API component | Technology choices within the approved architectural component |
| **Tool selection** | Select Stripe for payment processing | Specific tool choices within the approved component scope |

---

## What Operator-Like Generation May NOT Redefine

After preflight approval, the operator pipeline is PROHIBITED from:

| Prohibited Action | Why | Detection Method |
|------------------|-----|-----------------|
| **Changing target users** | CRI is frozen: `target_customer_or_user_class` is non-negotiable | Compare workspace PROJECT.md user description against CRI |
| **Changing business outcome** | CRI is frozen: `business_outcome_hypothesis` is non-negotiable | Compare workspace goals against CRI |
| **Changing monetization model** | CRI is frozen: `monetization_model` gates architectural components | Compare workspace payment/billing modules against CRI |
| **Adding excluded components** | `non_goals` are frozen: excluded capabilities stay excluded | Check workspace modules against preflight `non_goals` |
| **Removing approved components** | `minimal_inevitable_set` is frozen: every component must be present | Check workspace modules against `minimal_inevitable_set` |
| **Dropping acceptance criteria** | `acceptance_criteria` are frozen: every criterion must appear in QA | Compare workspace `qa/acceptance.md` against `PREFLIGHT_ACCEPTANCE.json` |
| **Reversing decisions** | `decisions` are frozen: recorded commitments are normative | Compare workspace architectural choices against `PREFLIGHT_DECISIONS.json` |
| **Ignoring ELS mitigations** | `els_risks` with `workspace_gen` stage must be addressed | Check workspace modules address all `workspace_gen` ELS items |

---

## What Happens If Generation Detects a Conflict

When the operator-like generation process produces a workspace decision that contradicts an approved preflight artifact:

### Conflict examples

- Preflight approves a `persistent_data_store` component. Operator decides to use only in-memory storage. **Conflict:** the minimal-inevitable set requires persistence.
- Preflight records `DEC-003: The system uses a relational database`. Operator selects a document database. **Conflict:** decision record is contradicted.
- Preflight acceptance includes `AC-007: Users can reset their password via email`. Operator omits the password-reset module. **Conflict:** acceptance criterion cannot be met.

### Conflict resolution protocol

1. **Stop generation immediately.** Do not continue building on a conflicted foundation.
2. **Identify the specific conflict:**
   - Which preflight artifact is contradicted (file name and field).
   - What the approved value is.
   - What the generation decision is.
   - Why they conflict.
3. **Present to the user with two options:**
   - **Reopen preflight:** Start a new preflight run from the phase whose output is contradicted. All downstream phases rerun. Previous approved artifacts are preserved.
   - **Accept deviation:** User explicitly approves the deviation. Record as a new decision in `PREFLIGHT_DECISIONS.json`:
     - New `decision_id` (next sequential DEC-NNN).
     - `decision_statement`: describes the deviation.
     - `owner_of_decision: user_explicit`.
     - `selected_rationale`: user's stated reason.
     - `reversibility_cost_if_wrong`: assessed by the agent.
4. **Resume generation only after resolution.** Either preflight is reopened (new run) or the deviation is recorded and acknowledged.

### What is NOT a conflict

- Operator choosing a specific technology within an approved architectural component (e.g., choosing PostgreSQL for the `persistent_data_store` component) is NOT a conflict — it is implementation detail within approved scope.
- Operator adding QA criteria beyond preflight acceptance is NOT a conflict — additional criteria are always allowed.
- Operator changing wave order from `PREFLIGHT_BUILD_ORDER.md` recommendation is NOT a conflict — build order is a recommendation, not a mandate.

---

## Whether Preflight Artifacts Become Normative Input for Forge/Bridge

**Yes.** The preflight artifact family is designed to become normative input for future forge/bridge integration:

- `PREFLIGHT_APPROVAL.json` is the gate artifact that forge must validate before executing generation.
- `PREFLIGHT_ACCEPTANCE.json` provides the acceptance criteria that bridge should cross-reference against the generated workspace's QA checklist.
- `PREFLIGHT_DECISIONS.json` provides the decision records that bridge should verify are not contradicted by workspace generation.
- `preflight-handoff.schema.json` is the validation schema that forge/bridge should use for programmatic validation.

In v1, the agent performs these checks manually. In v2+, forge/bridge code performs them automatically.

---

## How Workspace Generation References Preflight Artifacts

The generated workspace does NOT duplicate preflight artifacts. Instead:

1. **WORKSPACE.md** contains a "Preflight Reference" section pointing to the staging directory.
2. **PROJECT.md** incorporates CRI fields as project constraints (derived from `PREFLIGHT_PURPOSE.json`, not copy-pasted).
3. **qa/acceptance.md** is derived from `PREFLIGHT_ACCEPTANCE.json` — each acceptance criterion becomes a QA checklist item.
4. **state/orchestration.yaml** includes a `preflight_slug` field that records which preflight produced this workspace.

The staging directory (`v2/.buildr/preflight/<project-slug>/`) remains the source of truth for preflight artifacts. The workspace references them; it does not own them.

---

## How This Flow Remains One User Experience

From the user's perspective, the interaction is:

```
User: "Build me a booking site for fishing trips in Zanzibar"
  |
  v
[Agent runs preflight — user sees phase-by-phase progress]
  |
  v
[Agent reports approval or asks for more information]
  |
  v
[Agent generates workspace — user sees workspace creation]
  |
  v
User: "Run it" -> buildr-executor takes over
```

The user does not need to:
- Invoke preflight and generation separately.
- Manage staging directories.
- Read JSON payloads.
- Understand the five-phase pipeline.

The user sees one flow: describe -> (questions if needed) -> workspace. The internal staging is transparent to the user unless they want to inspect it.

### Internal phase boundaries are preserved

Although the user sees one flow, the internal phases are strictly separated:
- Each phase writes its own artifacts before the next phase begins.
- Binary gates are checked between phases.
- The pipeline can halt at any phase if a gate fails.
- The user is informed of the halt and asked for input or given a rejection explanation.

This is the key architectural property: one user experience, strict internal staging.

---

## How v2 Skills Are Discovered/Installed Relative to Existing Skills

### The install/discovery rule (single, unambiguous)

**`v2/skills/` is the source-of-truth in-repo path for v2 system skills.** Installation into the CLI/runtime requires one explicit action:

```bash
# Option A: Symlink (recommended for development)
ln -s "$(pwd)/v2/skills/buildr-workspace-architect" \
      "$(pwd)/skills/buildr-workspace-architect"

# Option B: Copy (for distribution/deployment)
cp -r v2/skills/buildr-workspace-architect skills/buildr-workspace-architect
```

After this step, the runtime discovers `buildr-workspace-architect` alongside `buildr-operator`, `buildr-executor`, `buildr-smith`, and `buildr-scout` in the existing `skills/` directory.

### Why this approach

- **`skills/` is the runtime-facing discovery path.** All existing system skills live there. The runtime (CLI, agent loader) scans `skills/` for `SKILL.md` files.
- **`v2/skills/` is the development/staging path.** New v2 skills are authored, reviewed, and tested here before being installed into the runtime path.
- **One discovery path, not two.** The runtime only scans `skills/`. It does not know about `v2/skills/`. This prevents ambiguity about which version of a skill is active.

### What this means for the user

1. Author/modify v2 skills in `v2/skills/`.
2. Install into `skills/` via symlink or copy.
3. Load the advanced operator prompt (`v2/prompts/buildr-advanced-operator.md`) in the CLI/runtime.
4. The advanced operator invokes `buildr-workspace-architect` from the standard `skills/` path.

### What this means for existing skills

- Existing skills in `skills/` are unaffected.
- `buildr-operator` remains available for basic/legacy workspace generation.
- `buildr-executor`, `buildr-smith`, and `buildr-scout` are unchanged.
- The advanced operator prompt uses `buildr-workspace-architect` for preflight and then delegates to operator-like generation (which reuses operator's Phases 2-5).

---

## Git, Retention, and Immutability Consistency

These rules are consistent across all v2 documents:

| Rule | Advanced Prompt | SKILL.md | approval.md | This File |
|------|----------------|----------|-------------|-----------|
| `v2/.buildr/` is gitignored by default | Yes | Yes | Yes | Yes |
| Approved artifacts are immutable unless reopened | Yes | Yes | Yes | Yes |
| Reruns overwrite non-approved artifacts | Yes | Yes | Yes | Yes |
| Reruns for approved slugs create timestamped variant | Yes | Yes | Yes | Yes |
| `PREFLIGHT_APPROVAL.json`/`DECISIONS.json`/`ACCEPTANCE.json` may be committed for audit | — | Yes | — | — |
| Abandoned artifacts are cleaned on next same-slug run | Yes | Yes | — | — |

No document contradicts another on these rules.

---

## Ground repository backlog (post-v2)

After the v2 skill and prompt exist in the repo, **`v2/improve.md`** lists optional work in the **rest of the repository** so preflight output becomes easier to validate, ingest into generated workspaces, and drive vault selection (schemas under repo root, `preflight_validate`, ingest maps, operator `references/`, template anchors, vault strategy/routine, docs). That backlog does **not** change the handoff rules in this file; it hardens the foundation around them.
