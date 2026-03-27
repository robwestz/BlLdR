# BUILDR SCOUT — System Architecture
## Knowledge Extraction × System Evolution × Cross-Pollination

> This document defines the Scout's internal architecture and its
> integration points with the rest of the Buildr system.

---

## The Core Insight

Agent systems rot in isolation. The Vault starts strong but drifts from
best practices. Strategies become outdated. New patterns emerge in the
field and the system doesn't absorb them. The Scout is the mechanism
that prevents this — it's the system's immune system AND its learning
system in one.

The Scout solves three problems:
1. **Knowledge decay** — vault items age; the Scout refreshes them
2. **Knowledge gaps** — new patterns emerge; the Scout absorbs them
3. **Knowledge silos** — insights from one article apply to multiple
   vault items; the Scout cross-pollinates

---

## Integration Points

### How Scout Connects to the System

```
                    ┌──────────────┐
                    │  External    │
                    │  Sources     │
                    │  (articles,  │
                    │  docs, repos)│
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │              │
                    │  SCOUT       │
                    │  (this skill)│
                    │              │
                    └──┬───┬───┬───┘
                       │   │   │
          ┌────────────┘   │   └────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │  VAULT    │   │  REPO     │   │  AGENTS   │
    │  (new/    │   │  (direct  │   │  (via      │
    │  updated  │   │  file     │   │  directives│
    │  items)   │   │  edits)   │   │  & briefs) │
    └───────────┘   └───────────┘   └───────────┘
```

### What Scout Reads (Input Dependencies)

| Component | What Scout Reads | Why |
|-----------|-----------------|-----|
| `vault/INDEX.md` | Full vault inventory | Cross-reference findings against existing items |
| `vault/skills/*.md` | Existing skills | Detect overlap, find upgrade candidates |
| `vault/constraints/*.md` | Existing constraints | Detect conflicts |
| `vault/strategies/*.md` | Existing strategies | Find gaps |
| `vault/memories/**/*.md` | Existing memories | Avoid duplicate scars/insights |
| `MANIFEST.md` | System inventory | Know what exists before creating |
| `catalog/index.json` | External tool catalog | Find related tools |
| `memory-system/continuum/discoveries.jsonl` | Past discoveries | Avoid re-discovering known things |
| `CLAUDE.md` | System guardrails | Respect existing rules |
| `engines/*.py` | Engine implementations | Understand capabilities before proposing changes |

### What Scout Writes (Output Destinations)

| Output Type | Destination | Reviewed By |
|------------|-------------|-------------|
| New vault items | `vault/[type]/[name].md` | Smith (quality gate) |
| Vault updates | In-place edits to `vault/**/*.md` | Smith (quality gate) |
| Repo modifications | Any repo file | Human (via diff) |
| Agent directives | `.tmp/directives/[slug].md` | Operator or target agent |
| Evolution proposals | `docs/proposals/[slug].md` | Human (decision required) |
| Discoveries | `memory-system/continuum/discoveries.jsonl` | Memory system (auto) |
| Manifest updates | `MANIFEST.md` | Self (append) |

---

## The Analysis Engine

### Depth Levels

The Scout operates at three depth levels based on context:

#### Quick Scan (1-2 minutes)
- Single source, narrow scope
- Extract top 3 findings
- Map to existing vault items
- Produce: upgrades or 1 new item

**When:** User says "check this article" or "what does this say about X?"

#### Standard Analysis (5-10 minutes)
- Single source, full analysis
- All extraction dimensions
- Cross-reference with vault
- Gap detection
- Produce: multiple vault items + repo modifications

**When:** User provides an article and says "absorb this" or "extract value"

#### Deep Research (15-30 minutes)
- Multiple sources or complex topic
- Full analysis + lateral discovery
- Cross-source synthesis
- System-wide impact assessment
- Produce: vault items + directives + evolution proposals

**When:** User says "research [topic]" or "investigate how we should handle [X]"

### Depth Selection Logic

```
If user provides URL/article + asks specific question → Quick Scan
If user provides URL/article + asks to absorb/extract → Standard Analysis
If user asks to research a topic (no specific source) → Deep Research
If user provides multiple sources → Deep Research
If explicit: "quick look" / "snabbtitt" → Quick Scan
If explicit: "deep dive" / "gå på djupet" → Deep Research
Default → Standard Analysis
```

---

## Source Processing Strategies

### For Engineering Blog Posts (like Anthropic, Vercel, etc.)

```
1. Identify: What problem does the author solve?
2. Extract: What specific technique/pattern did they use?
3. Generalize: Strip away the author's specific context
4. Test: Does this generalized pattern pass the agnosticism test?
5. Emit: Skill (if it's how-to), Strategy (if it's decision framework),
         Constraint (if it's what-not-to-do), Memory (if it's experience)
```

### For Documentation / API References

```
1. Identify: What capability does this document?
2. Extract: Usage patterns, gotchas, configuration options
3. Map: Which existing vault items reference this technology?
4. Emit: Update existing skills with new details, or create new skill
         if technology is entirely new to the system
```

### For Research Papers / Technical Deep Dives

```
1. Identify: What's the core thesis?
2. Extract: Concrete findings (numbers, benchmarks, comparisons)
3. Translate: Convert academic language to practitioner language
4. Assess: How mature is this? Production-ready or experimental?
5. Emit: Strategy (if decision framework), Evolution Proposal (if
         architectural), Memory/Insight (if validated approach)
```

### For Codebases / Open Source Projects

```
1. Map: Architecture, key patterns, file structure
2. Extract: Patterns worth replicating, anti-patterns to avoid
3. Compare: How does their approach differ from Buildr's?
4. Emit: Skills (how they do things we should do),
         Constraints (mistakes they made we should avoid),
         Catalog entries (if the tool is usable by Buildr agents)
```

---

## Cross-Pollination Engine

The most valuable Scout operation: connecting knowledge across sources.

### How It Works

```
Article A discusses "generator-evaluator pattern"
  ↓
Scout processes Article A → extracts pattern
  ↓
Scout searches vault: "Do we have QA feedback loops?"
  ↓
Finds: vault/routines/post-module-qa.md exists but is one-pass
  ↓
Scout identifies: post-module-qa.md could be upgraded with
  iterative evaluation cycles inspired by Article A
  ↓
Scout emits: upgrade to post-module-qa.md + new strategy
  "iterative-qa.md" describing when single-pass vs multi-pass QA
```

### Cross-Pollination Rules

1. **Never copy.** Translate concepts into Buildr's language and format.
2. **Always credit.** The source finding links back to the article.
3. **Prefer upgrades over new items.** A stronger existing item beats
   a new item that overlaps.
4. **Flag conflicts.** If a finding contradicts an existing vault item,
   don't silently override. Present both to the human.

---

## The Research Mode

When the user asks the Scout to research a topic (not process a specific
source), the Scout follows this protocol:

### Research Protocol

```
1. SCOPE — Define what we're researching and why
   Ask the user if scope is unclear. Max 2 questions.

2. AUDIT — What does the Buildr system already know about this?
   Read relevant vault items, strategies, memories.

3. GATHER — Collect source material
   Use WebFetch for known URLs.
   Use WebSearch for discovery (if available).
   Read relevant files in the repo.
   Check catalog/index.json for related tools.

4. SYNTHESIZE — Cross-reference sources against each other
   Identify consensus, contradictions, gaps.

5. RECOMMEND — Produce prioritized action list
   What should change in the system?
   What requires human decision?
   What can be auto-applied?

6. EMIT — Produce artifacts (same as standard pipeline Phase 5)
```

### Research Quality Gate

A research output must:
- Reference at least 2 independent sources (or explain why only 1 exists)
- Identify at least 1 thing the system currently does wrong or doesn't do
- Produce at least 1 concrete artifact (not just a report)
- State what it COULDN'T find or verify (intellectual honesty)

---

## Interaction with Other Skills

### Scout → Smith

The Scout proposes vault items. The Smith validates them.

```
Scout produces: vault/skills/evaluator-tuning.md (draft)
Smith validates: agnosticism test, line limits, template compliance
Result: approved item enters the vault
```

In practice, the Scout should self-apply Smith's quality gate during
Phase 5 (Emit). But if the user runs both skills in sequence, Smith
acts as the final reviewer.

### Scout → Operator

The Scout produces knowledge. The Operator consumes it.

```
Scout finds: "Sprint contracts improve multi-agent coordination"
Scout emits: vault/strategies/sprint-contracts.md
Later: Operator generates a workspace that includes sprint-contracts
       in the vault-selection for the QA wave
```

### Scout → Memory System

Every Scout session produces discoveries.

```
Scout processes article → logs 5 discoveries
memory-system distills → 3 unique insights
memory-inject → MEMORY.md updated
Next wave → agents benefit from new knowledge
```

---

## Anti-Patterns (What the Scout Must NOT Do)

### 1. Summarize Without Extracting
The user can read the article. The Scout's job is to produce ARTIFACTS,
not summaries. If the output is just "here's what the article says,"
the Scout has failed.

### 2. Create Overlapping Vault Items
Before creating ANY new vault item, check the existing inventory.
Prefer upgrading an existing item over creating a near-duplicate.

### 3. Auto-Execute Architectural Changes
The Scout can directly edit vault items and small repo files.
It MUST NOT modify engines, templates, or system architecture without
producing an evolution proposal first.

### 4. Ignore Conflicts
If a finding contradicts an existing vault item, the Scout MUST flag
the conflict explicitly. Silent overrides create system inconsistency.

### 5. Produce Non-Agnostic Vault Items
Everything in the vault must work for any project type. If a finding
is technology-specific, it goes to `vault/memories/stack/[tech].md`,
NOT to a general skill or constraint.

### 6. Research Without Bounds
Deep research must have a scope. If the user asks "research everything
about AI agents," the Scout asks for scope before spending 30 minutes.
Max 2 clarifying questions.

---

## Example: Processing the Harness Design Article

To illustrate the full pipeline, here's how the Scout would process
the Anthropic "Harness Design for Long-Running Apps" article:

### Phase 2 Output (Analyze)

**Patterns extracted:**
- Generator-Evaluator separation (strategy: feedback-loops)
- Sprint contracts (strategy: work-negotiation)
- File-based agent communication (skill: agent-handoff)
- Context resets at boundaries (strategy: context-management)
- Evaluator tuning through trace analysis (skill: evaluator-calibration)

**Anti-patterns extracted:**
- Self-evaluation bias (constraint: no-self-evaluation)
- Context window degradation on long tasks (memory/scar)
- Evaluator that approves everything (memory/scar)

**Principles extracted:**
- "Every harness component encodes an assumption about model limits"
- "Simplify harness as model improves" (strategy: harness-evolution)
- Prompt wording shapes output before feedback loops activate

### Phase 3 Output (Research)

**Cross-reference results:**
- `vault/routines/post-module-qa.md` — single-pass QA, could benefit
  from iterative evaluator pattern → FLAG FOR UPGRADE
- `vault/strategies/decomposition.md` — covers task decomposition but
  not generator/evaluator separation → FLAG FOR UPGRADE
- `templates/circuit-breaker.md` — exists, validates sprint contract idea
- No vault item covers "context reset at boundaries" → GAP

**Gap identified:**
- System lacks strategy for when to add/remove orchestration scaffolding
- No vault item for multi-agent evaluation patterns
- Imperfektum doesn't model evaluator-specific memories

### Phase 5 Output (Emit)

1. NEW: `vault/strategies/harness-evolution.md`
   — When to add/remove agent scaffolding based on model capability

2. UPDATE: `vault/routines/post-module-qa.md`
   — Add iterative evaluation option for complex modules

3. NEW: `vault/strategies/generator-evaluator.md`
   — When to split generation from evaluation

4. NEW: `vault/memories/universal-scars.md` (append)
   — Scar: "self-evaluation always passes" consequence

5. DIRECTIVE: `.tmp/directives/2026-03-27-evaluator-tuning.md`
   — Instructions for adding evaluator calibration to the orchestrator

6. PROPOSAL: `docs/proposals/2026-03-27-sprint-contracts.md`
   — Proposal to add sprint contract mechanism to wave orchestration
