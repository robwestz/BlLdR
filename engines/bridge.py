"""
FORGE × INDEX × IMPERFEKTUM — The Bridge
==========================================
"The agent remembers what it built, how it built it, and which tools it used."

Connects three systems:
- Project Forge   → WHAT to build (blueprint from human onboarding)
- The Index       → WHAT TOOLS exist (catalog of skills, packs, tools)
- Imperfektum     → WHAT THE AGENT REMEMBERS (fabricated episodic memory)

The bridge produces a WORKSPACE — a ready-to-execute folder that contains:
1. Forge scaffold     (PROJECT.md, SYSTEM.md, RUNBOOK.md, modules/, qa/)
2. Imperfektum memory (MEMORY.md)
3. Index-derived pack (relevant tools/skills for this specific project)
4. WORKSPACE.md       (ties everything together — the agent's launch file)

Usage:
    from bridge import WorkspaceBuilder

    builder = WorkspaceBuilder(
        index_catalog="the_index/catalog/index.json",
    )

    # Option A: From existing Forge blueprint
    workspace = builder.from_blueprint(blueprint, output_dir="./my-project")

    # Option B: From scratch (runs Forge onboarding internally)
    workspace = builder.from_description(
        description="Bokningssajt för fisketurer i Zanzibar, blåaktig",
        output_dir="./my-project"
    )
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import the engines
try:
    from .forge_engine import (
        ProjectForge, ScaffoldGenerator
    )
except ImportError:
    try:
        from forge_engine import (
            ProjectForge, ScaffoldGenerator
        )
    except ImportError:
        ProjectForge = None
        ScaffoldGenerator = None

try:
    from .imperfektum_engine import ImperfektumEngine, Scar, Insight
except ImportError:
    try:
        from imperfektum_engine import ImperfektumEngine, Scar, Insight
    except ImportError:
        ImperfektumEngine = None
        Scar = None
        Insight = None

try:
    from .vault_selector import select_for_wave
except ImportError:
    try:
        from vault_selector import select_for_wave
    except ImportError:
        select_for_wave = None


# =============================================================================
# INDEX RESOLVER — Finds relevant tools from The Index for a project
# =============================================================================

class IndexResolver:
    """
    Queries The Index's catalog and selects tools/skills relevant
    to the current project. Based on pack_builder.py's synonymity
    concept but adapted for project-type matching instead of
    mission-goal matching.
    """

    # Maps project categories to Index catalog domains/tags that are relevant
    CATEGORY_TO_INDEX_SIGNALS = {
        "booking": ["ui", "design", "frontend", "workflow", "orchestration"],
        "website": ["ui", "design", "frontend", "seo"],
        "e-commerce": ["ui", "design", "frontend", "workflow"],
        "web-app": ["ui", "design", "frontend", "workflow", "orchestration"],
        "saas": ["ui", "design", "frontend", "workflow", "orchestration", "multi-model"],
        "tool": ["workflow", "orchestration", "agent-methodology"],
        "api": ["orchestration", "mcp", "multi-model"],
    }

    # Tools from the Index that are ALWAYS relevant regardless of project type
    UNIVERSAL_TOOLS = [
        "constraint-mapper",      # Every project has constraints
        "pipeline-composer",      # Every project has build phases
        "retrospective-builder",  # Maps to Imperfektum's domain
    ]

    # Tools relevant only for specific contexts
    CONDITIONAL_TOOLS = {
        "blueprint-forge": lambda spec: True,  # Always useful
        "ui-ux-pro-max-skill": lambda spec: spec.category.value in (
            "website", "booking", "e-commerce", "web-app", "saas"),
        "superclaude-framework": lambda spec: True,  # Methodology always helps
        "agent-rules": lambda spec: True,  # Rules always relevant
    }

    def __init__(self, catalog_path: str = None):
        self.catalog = self._load_catalog(catalog_path) if catalog_path else {"items": []}

    def _load_catalog(self, path: str) -> dict:
        p = Path(path)
        if not p.exists():
            return {"items": []}
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def resolve(self, spec) -> List[Dict[str, Any]]:
        """Find relevant Index items for this project."""
        category = spec.category.value if hasattr(spec.category, 'value') else str(spec.category)
        selected = []
        seen_ids = set()

        # 1. Universal tools
        for tool_id in self.UNIVERSAL_TOOLS:
            item = self._find_item(tool_id)
            if item and item["id"] not in seen_ids:
                item["_selection_reason"] = "Universal tool — relevant for all projects"
                selected.append(item)
                seen_ids.add(item["id"])

        # 2. Conditional tools
        for tool_id, condition in self.CONDITIONAL_TOOLS.items():
            if condition(spec):
                item = self._find_item(tool_id)
                if item and item["id"] not in seen_ids:
                    item["_selection_reason"] = f"Matched condition for {category}"
                    selected.append(item)
                    seen_ids.add(item["id"])

        # 3. Tag/domain matching
        signals = self.CATEGORY_TO_INDEX_SIGNALS.get(category, [])
        for item in self.catalog.get("items", []):
            if item["id"] in seen_ids:
                continue
            item_tags = set(item.get("tags", []))
            item_domains = set(item.get("domain", []))
            overlap = item_tags.union(item_domains).intersection(set(signals))
            if overlap:
                resolved_item = dict(item)
                resolved_item["_selection_reason"] = f"Tag/domain match: {sorted(overlap)}"
                selected.append(resolved_item)
                seen_ids.add(item["id"])

        return selected

    def _find_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        for item in self.catalog.get("items", []):
            if item["id"] == item_id:
                return dict(item)  # Copy to avoid mutation
        return None


# =============================================================================
# TOOL-AWARE MEMORY GENERATOR — Extends Imperfektum with Index knowledge
# =============================================================================

class ToolAwareMemoryGenerator:
    """
    Extends Imperfektum's memory with 'experiences' of using specific
    tools from The Index. The agent doesn't just remember building the
    project — it remembers WHICH TOOLS it used and how they helped.
    """

    # Fabricated experiences per Index tool
    if Scar is not None and Insight is not None:
        TOOL_MEMORIES = {
            "constraint-mapper": {
                "scars": [
                    Scar(
                        "During project planning",
                        "We started building without mapping constraints first",
                        "Halfway through, we discovered conflicting requirements that forced a redesign of two modules",
                        "Run Constraint Mapper BEFORE building. Map every hard constraint and verify they don't conflict."
                    ),
                ],
                "insights": [
                    Insight(
                        "Project planning",
                        "We used Constraint Mapper to decompose the project goal into acceptance criteria before writing any code",
                        "Every module had clear, testable criteria from day one. QA was trivial because we knew exactly what 'done' meant.",
                        "Run Constraint Mapper on PROJECT.md before starting RUNBOOK.md. Each constraint should map to at least one QA check."
                    ),
                ],
            },
            "pipeline-composer": {
                "scars": [
                    Scar(
                        "Module ordering",
                        "We tried to optimize the build order ourselves instead of following the composed pipeline",
                        "We built the payment module before the booking flow was stable. Had to rewire everything.",
                        "Trust the Pipeline Composer's dependency ordering. It exists because modules have real dependencies."
                    ),
                ],
                "insights": [
                    Insight(
                        "Build phases",
                        "Pipeline Composer's staged gate approach meant we never started a module before its dependencies were QA'd",
                        "Zero cascading failures. Each stage was solid before the next began.",
                        "Follow the pipeline stages exactly. The gates exist for a reason."
                    ),
                ],
            },
            "retrospective-builder": {
                "insights": [
                    Insight(
                        "After each module",
                        "We ran a quick retrospective after each module (what worked, what didn't, what to change)",
                        "Each subsequent module was built better than the last. Lessons from module 2 improved module 3.",
                        "After completing each module's QA, spend 30 seconds noting what went well and what to avoid next."
                    ),
                ],
            },
            "blueprint-forge": {
                "insights": [
                    Insight(
                        "Module specifications",
                        "Blueprint Forge generated detailed module specs with exact file lists, component hierarchies, and data models",
                        "When we started each module, we already knew exactly which files to create and how they connected.",
                        "Read the full module spec before writing any code. The blueprint eliminates guesswork."
                    ),
                ],
            },
            "ui-ux-pro-max-skill": {
                "insights": [
                    Insight(
                        "UI implementation",
                        "We loaded the UI/UX Pro Max skill before building any visual components",
                        "The skill's design patterns prevented the typical 'AI-generated UI' look. Components felt handcrafted.",
                        "Activate the UI/UX skill during the design system and every visual module. It transforms generic into polished."
                    ),
                ],
                "scars": [
                    Scar(
                        "Component styling",
                        "We built the first three components without the UI/UX skill",
                        "They looked like default Tailwind — functional but generic. We had to restyle them after loading the skill.",
                        "Load the UI/UX skill BEFORE building any component. Retrofitting design is twice the work."
                    ),
                ],
            },
            "superclaude-framework": {
                "insights": [
                    Insight(
                        "Agent methodology",
                        "SuperClaude's persona system gave us clear modes for different tasks — architect mode for planning, code mode for building, review mode for QA",
                        "Each phase got the right type of thinking. Planning wasn't mixed with implementation.",
                        "Use architect mode for RUNBOOK planning, code mode for module building, review mode for QA."
                    ),
                ],
            },
            "agent-rules": {
                "insights": [
                    Insight(
                        "Development discipline",
                        "We loaded the agent-rules pack at project start which gave us clear boundaries on what to do and what not to do",
                        "No wasted time on patterns that would be rejected later. The rules prevented common anti-patterns upfront.",
                        "Read agent-rules at session start. They complement SYSTEM.md with implementation-level constraints."
                    ),
                ],
            },
        }
    else:
        TOOL_MEMORIES = {}

    def generate_tool_memories(self, selected_tools: List[Dict[str, Any]]) -> str:
        """Generate memory section about tools used."""
        if not selected_tools:
            return ""

        sections = []
        sections.append("\n## Tools We Used (and How They Helped)\n")
        sections.append("Last time we built this project, we had these tools available. "
                        "Here's what we learned about each one.\n")

        for tool in selected_tools:
            tool_id = tool["id"]
            tool_name = tool.get("name", tool_id)
            memories = self.TOOL_MEMORIES.get(tool_id, {})

            sections.append(f"\n### {tool_name}\n")
            sections.append(f"Source: `{tool.get('source', 'unknown')}`\n")

            if "insights" in memories:
                for ins in memories["insights"]:
                    sections.append(f"**What worked:** {ins.what_worked}\n")
                    sections.append(f"→ {ins.apply_again}\n")

            if "scars" in memories:
                for scar in memories["scars"]:
                    sections.append(f"**Mistake we made:** {scar.what_happened}\n")
                    sections.append(f"→ {scar.lesson}\n")

            if not memories:
                sections.append(f"Available for this project. "
                                f"Tags: {', '.join(tool.get('tags', []))}\n")

        return "\n".join(sections)


# =============================================================================
# WORKSPACE BUILDER — The Main Orchestrator
# =============================================================================

class WorkspaceBuilder:
    """
    Produces a complete, ready-to-execute workspace by combining:
    1. Forge scaffold (build instructions)
    2. Index-selected tools (relevant capabilities)
    3. Imperfektum memory (fabricated experience)
    4. Workspace manifest (ties everything together)
    """

    def __init__(self, index_catalog: str = None):
        self.index_resolver = IndexResolver(index_catalog)
        self.tool_memory_gen = ToolAwareMemoryGenerator()
        self.imperfektum = ImperfektumEngine() if ImperfektumEngine else None

    def _selector_category(self, spec) -> str:
        category = spec.category.value if hasattr(spec.category, "value") else str(spec.category)
        return {
            "e-commerce": "ecommerce",
            "web-app": "webapp",
        }.get(category, category)

    def _selector_stack(self, spec) -> str:
        stack = spec.tech_stack.value if hasattr(spec.tech_stack, "value") else str(spec.tech_stack)
        if stack.startswith("python-"):
            return "python"
        return stack

    def _resolve_wave_selection(self, blueprint) -> Dict[str, List[str]]:
        if not select_for_wave or not getattr(blueprint, "modules", None):
            return {"skills": [], "constraints": [], "routines": [], "memories": []}

        first_module = min(blueprint.modules, key=lambda module: module.order)
        intent = f"{first_module.name} {first_module.description}".strip()
        return select_for_wave(
            intent=intent,
            tier="B",
            category=self._selector_category(blueprint.spec),
            stack=self._selector_stack(blueprint.spec),
        )

    def _write_vault_selection(self, out: Path, blueprint) -> List[str]:
        selection = self._resolve_wave_selection(blueprint)
        selection_dir = out / "vault-selection"
        selection_dir.mkdir(exist_ok=True)
        selection_path = selection_dir / "001-foundation.json"
        selection_path.write_text(
            json.dumps(selection, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        wave_path = out / "waves" / "001-foundation.md"
        if wave_path.exists():
            wave = wave_path.read_text(encoding="utf-8")
            relative_items = []
            repo_root = Path(__file__).resolve().parent.parent
            for group in ("skills", "constraints", "routines", "memories"):
                for item in selection.get(group, []):
                    try:
                        relative_items.append(str(Path(item).relative_to(repo_root)).replace("\\", "/"))
                    except ValueError:
                        relative_items.append(str(item).replace("\\", "/"))

            block = "## Vault Items\nLoad these before executing:\n"
            if relative_items:
                block += "\n".join(f"- {item}" for item in relative_items)
            else:
                block += "- (none selected for this wave)"

            if "## Vault Items" in wave and "\n## Steps" in wave:
                before, remainder = wave.split("## Vault Items", 1)
                _, after = remainder.split("\n## Steps", 1)
                wave = before + block + "\n\n## Steps" + after
                wave_path.write_text(wave, encoding="utf-8")

        return [str(selection_path)]

    def from_blueprint(self, blueprint, output_dir: str) -> List[str]:
        """Build workspace from an existing Forge blueprint."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        files = []

        # 1. Generate Forge scaffold
        if not ScaffoldGenerator:
            raise ImportError("forge_engine.py required for from_blueprint()")

        gen = ScaffoldGenerator()
        files.extend(gen.generate(blueprint, output_dir))

        files.extend(self._write_vault_selection(out, blueprint))

        # 2. Resolve relevant Index tools
        selected_tools = self.index_resolver.resolve(blueprint.spec)

        # 3. Generate Imperfektum memory (base)
        base_memory = ""
        if self.imperfektum:
            base_memory = self.imperfektum.generate(blueprint)

        # 4. Generate tool-aware memory extension
        tool_memory = self.tool_memory_gen.generate_tool_memories(selected_tools)

        # 5. Combine memories
        combined_memory = base_memory
        if tool_memory:
            # Insert tool memories before the "How to Use This Memory" section
            if "## How to Use This Memory" in combined_memory:
                combined_memory = combined_memory.replace(
                    "## How to Use This Memory",
                    tool_memory + "\n---\n\n## How to Use This Memory"
                )
            else:
                combined_memory += "\n" + tool_memory

        # Write combined MEMORY.md
        memory_path = out / "MEMORY.md"
        memory_path.write_text(combined_memory, encoding="utf-8")
        files.append(str(memory_path))

        # 6. Generate WORKSPACE.md
        workspace_path = out / "WORKSPACE.md"
        workspace_path.write_text(
            self._render_workspace(blueprint, selected_tools),
            encoding="utf-8"
        )
        files.append(str(workspace_path))

        # 7. Generate tool manifest
        tools_path = out / "TOOLS.md"
        tools_path.write_text(
            self._render_tools(selected_tools, blueprint.spec),
            encoding="utf-8"
        )
        files.append(str(tools_path))

        # 8. Patch AGENT.md to include new files
        self._patch_agent(out, selected_tools)

        return files

    def from_description(self, description: str, output_dir: str,
                         audience: str = "", feeling: str = "",
                         color: str = "", location: str = "",
                         level: str = "standard") -> List[str]:
        """Build workspace from a plain-text project description."""
        if not ProjectForge:
            raise ImportError("forge_engine.py required for from_description()")

        forge = ProjectForge()
        try:
            forge.onboarding.spec.level = type(forge.onboarding.spec.level)(level)
        except (ValueError, TypeError, AttributeError):
            pass

        # Run minimal onboarding
        forge.process_answer("what", "", description, ["category"])
        if audience:
            forge.process_answer("who_for", "", audience, ["target_audience"])
        if feeling:
            forge.process_answer("feeling", "", feeling, ["feeling"])
        if color:
            forge.process_answer("brand", "", color, ["color_hint"])

        # Derive location signals
        if location:
            forge.onboarding.spec.audience_location = location.lower()
            if location.lower() in ("zanzibar", "africa"):
                forge.onboarding.spec.audience_device = "mobile-first"

        blueprint = forge.create_blueprint()
        return self.from_blueprint(blueprint, output_dir)

    def _render_workspace(self, blueprint, selected_tools: list) -> str:
        """Generate WORKSPACE.md — the master document."""
        spec = blueprint.spec
        category = spec.category.value if hasattr(spec.category, 'value') else str(spec.category)
        stack = spec.tech_stack.value if hasattr(spec.tech_stack, 'value') else str(spec.tech_stack)
        tool_names = [t.get("name", t["id"]) for t in selected_tools]
        ui_categories = {"website", "booking", "e-commerce", "web-app", "saas"}
        evaluator_note = (
            "UI evaluator review should use browser/Playwright-style validation when the tools are available."
            if category in ui_categories
            else "Evaluator review should focus on contracts, code quality, failure handling, and operational usability."
        )

        return f"""# WORKSPACE: {spec.project_name or spec.description[:50]}

> Generated by Forge × Index × Imperfektum
> {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## What This Workspace Contains

| File | Purpose | Read When |
|------|---------|-----------|
| **WORKSPACE.md** | This file — overview | First |
| **PROJECT.md** | What to build, constraints | Before starting |
| **SYSTEM.md** | Design system, code standards | Before starting |
| **MEMORY.md** | Your experience from last time | Before starting |
| **TOOLS.md** | Available tools from the Index | Reference as needed |
| **AGENT.md** | Builder behavior rules | At session start |
| **EVALUATOR.md** | Evaluator review rules and criteria | Before reviewing output |
| **RUN.md** | Canonical execution loop | During build |
| **state/orchestration.yaml** | Progress, budgets, wave status | Each session |
| **waves/** | Current wave specs and vault loads | Per wave |
| **contracts/** | Locked interfaces and decisions | When touching boundaries |
| **RUNBOOK.md** | Supplemental module detail | During build |
| **modules/** | Per-module specifications | Per module |
| **qa/** | Quality checklists | After each module |
| **qa/evaluations/** | Evaluator feedback artifacts | After each completed wave/module |

---

## Project Summary

- **Type:** {category}
- **Stack:** {stack}
- **Modules:** {len(blueprint.modules)}
- **Feeling:** {spec.feeling or "professional"}
- **Languages:** {", ".join(spec.languages)}
- **Export-ready:** Yes

---

## Available Tools (from The Index)

{chr(10).join(f"- **{name}**" for name in tool_names)}

These tools were selected because they are relevant to this project type.
See TOOLS.md for details on each one.

---

## Execution Order

1. Read AGENT.md and WORKSPACE.md to understand the file contract.
2. Read PROJECT.md and SYSTEM.md to understand what to build and how to build it.
3. Read MEMORY.md and TOOLS.md before starting.
4. Follow RUN.md as the canonical loop using state/orchestration.yaml and waves/.
5. Evaluator reviews each completed wave/module and writes advisory feedback.
6. Use RUNBOOK.md only as supplemental per-module detail.
7. QA after every module and re-read MEMORY.md's completion criteria before declaring done.

---

## The Imperfektum Principle

You have built this project before. MEMORY.md contains your notes from
last time. The mistakes listed there are real mistakes you made. The
insights are real things that worked. The vision of the finished product
is what the client actually received and approved.

Use this memory. Don't repeat the mistakes. Replicate the insights.
Deliver the product you remember delivering.

---

## Evaluator Default

This workspace uses a default builder/evaluator pattern.
The evaluator is advisory, not automatically blocking, but its feedback is expected to shape the next iteration.

{evaluator_note}

---

*Workspace generated by buildr.nu*
"""

    def _render_tools(self, selected_tools: list, spec=None) -> str:
        """Generate TOOLS.md — catalog of available tools."""
        sections = ["# Available Tools\n"]
        sections.append("> Tools selected from The Index for this project.\n")
        sections.append("> Install/activate these as needed during the build.\n\n---\n")
        category = ""
        if spec is not None:
            category = spec.category.value if hasattr(spec.category, "value") else str(spec.category)
        ui_categories = {"website", "booking", "e-commerce", "web-app", "saas"}
        evaluator_line = (
            "- For UI projects, evaluator should use browser/Playwright-style validation when those tools are available.\n\n---\n"
            if category in ui_categories
            else "- For non-UI projects, evaluator should focus on contracts, code quality, failure handling, and operational usability.\n\n---\n"
        )
        sections.append("## Default Workspace Roles\n\n")
        sections.append("- **Builder** — implements the active wave/module.\n")
        sections.append("- **Evaluator** — reviews completed work and writes advisory feedback.\n")
        sections.append(evaluator_line)

        for tool in selected_tools:
            tool_id = tool["id"]
            tool_name = tool.get("name", tool_id)
            tags = ", ".join(tool.get("tags", []))
            source = tool.get("source", "unknown")
            roles = ", ".join(tool.get("role", []))
            reason = tool.get("_selection_reason", "")
            entry = tool.get("entrypoints", [])

            sections.append(f"""## {tool_name}

- **ID:** `{tool_id}`
- **Role:** {roles}
- **Tags:** {tags}
- **Source:** `{source}`
- **Entry points:** {", ".join(f"`{e}`" for e in entry)}
- **Why selected:** {reason}

---
""")

        sections.append("\n*Selected by Index Resolver from buildr.nu catalog*\n")
        return "\n".join(sections)

    def _patch_agent(self, out: Path, selected_tools: list):
        """Patch AGENT.md to include MEMORY.md, TOOLS.md, and WORKSPACE.md."""
        agent_path = out / "AGENT.md"
        if not agent_path.exists():
            return

        content = agent_path.read_text(encoding="utf-8")

        # Only patch if not already patched
        if "WORKSPACE.md" in content:
            return

        # Replace reading order
        content = content.replace(
            "| 1 | **PROJECT.md** | Hard constraints, modulöversikt, teknisk stack |",
            "| 0 | **WORKSPACE.md** | Master overview — read this FIRST |\n"
            "| 1 | **PROJECT.md** | Hard constraints, modulöversikt, teknisk stack |"
        )

        if "MEMORY.md" not in content:
            content = content.replace(
                "| 3 | **RUNBOOK.md**",
                "| 3 | **MEMORY.md** | Your experience — mistakes to avoid, what worked |\n"
                "| 4 | **TOOLS.md** | Available tools from The Index |\n"
                "| 5 | **RUNBOOK.md**"
            )
            content = content.replace(
                "| 4 | **modules/",
                "| 6 | **modules/"
            )

        agent_path.write_text(content, encoding="utf-8")


# =============================================================================
# CLI
# =============================================================================

def main():
    import sys

    print("\n" + "=" * 60)
    print("  FORGE × INDEX × IMPERFEKTUM")
    print("  Complete workspace builder")
    print("=" * 60)

    # Check dependencies
    if not ProjectForge:
        print("\n  ERROR: forge_engine.py not found in current directory")
        sys.exit(1)
    if not ImperfektumEngine:
        print("\n  ERROR: imperfektum_engine.py not found in current directory")
        sys.exit(1)

    # Find index catalog
    catalog_path = None
    for candidate in [
        "the_index/catalog/index.json",
        "catalog/index.json",
        "index.json",
    ]:
        if Path(candidate).exists():
            catalog_path = candidate
            break

    if catalog_path:
        print(f"\n  Index catalog: {catalog_path}")
    else:
        print("\n  WARNING: No Index catalog found. Tool selection disabled.")

    # Build workspace
    builder = WorkspaceBuilder(index_catalog=catalog_path)

    print("\n  Describe your project:")
    description = input("  > ").strip()
    if not description:
        print("  No description provided. Exiting.")
        sys.exit(0)

    print("\n  Who is it for?")
    audience = input("  > ").strip()

    print("\n  How should it feel? (professional, playful, minimal, warm, etc.)")
    feeling = input("  > ").strip()

    print("\n  Any color preference? (blue, red, green, etc.)")
    color = input("  > ").strip()

    print("\n  Location/context? (e.g., sweden, zanzibar, global)")
    location = input("  > ").strip()

    output_dir = input("\n  Output folder [./workspace]: ").strip() or "./workspace"

    files = builder.from_description(
        description=description,
        audience=audience,
        feeling=feeling,
        color=color,
        location=location,
        output_dir=output_dir,
    )

    print(f"\n{'=' * 60}")
    print("  WORKSPACE GENERATED")
    print(f"{'=' * 60}")
    print(f"\n  {len(files)} files in {output_dir}/")
    print("\n  New files (beyond standard Forge):")
    for f in sorted(files):
        name = Path(f).name
        if name in ("WORKSPACE.md", "MEMORY.md", "TOOLS.md"):
            print(f"    ✦ {name}")

    print("\n  Next steps:")
    print(f"  1. Point your LLM agent at {output_dir}/")
    print("  2. Tell it: 'Read WORKSPACE.md, then follow AGENT.md'")
    print("  3. The project builds itself.")
    print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    main()
