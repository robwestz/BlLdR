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
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

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
# PREFLIGHT INGESTOR — Loads approved preflight into workspace generation
# =============================================================================

class PreflightError(Exception):
    """Raised when preflight artifacts are invalid or incomplete."""
    pass


class PreflightIngestor:
    """
    Loads and validates approved preflight artifacts, making them available
    as normative constraints for workspace generation.

    Production-grade: validates existence, JSON validity, approval status,
    required fields, and cross-references before returning any data.
    Fails loudly on any inconsistency — never silently degrades.
    """

    REQUIRED_ARTIFACTS = [
        "PREFLIGHT_PURPOSE.md", "PREFLIGHT_PURPOSE.json",
        "PREFLIGHT_ABSENCE_MAP.md", "PREFLIGHT_ABSENCE_MAP.json",
        "PREFLIGHT_ARCHITECTURE.md", "PREFLIGHT_ARCHITECTURE.json",
        "PREFLIGHT_CHALLENGE.md", "PREFLIGHT_CHALLENGE.json",
        "PREFLIGHT_APPROVAL.md", "PREFLIGHT_APPROVAL.json",
        "PREFLIGHT_DECISIONS.md", "PREFLIGHT_DECISIONS.json",
        "PREFLIGHT_ACCEPTANCE.md", "PREFLIGHT_ACCEPTANCE.json",
        "PREFLIGHT_BUILD_ORDER.md",
    ]

    JSON_ARTIFACTS = [a for a in REQUIRED_ARTIFACTS if a.endswith(".json")]

    def __init__(self, preflight_dir: str):
        self.dir = Path(preflight_dir)
        self._payloads: Dict[str, Any] = {}
        self._validated = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_and_load(self) -> None:
        """Validate all artifacts and load JSON payloads.

        Raises PreflightError with a detailed message on any failure.
        After this returns, all payloads are available via properties.
        """
        errors: List[str] = []

        # 1. Directory exists
        if not self.dir.is_dir():
            raise PreflightError(
                f"Preflight staging directory does not exist: {self.dir}"
            )

        # 2. All required artifacts exist
        for artifact in self.REQUIRED_ARTIFACTS:
            path = self.dir / artifact
            if not path.exists():
                errors.append(f"Missing artifact: {artifact}")
            elif path.stat().st_size == 0:
                errors.append(f"Empty artifact: {artifact}")

        if errors:
            raise PreflightError(
                f"Preflight artifacts incomplete ({len(errors)} issues):\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

        # 3. Parse all JSON artifacts
        for artifact in self.JSON_ARTIFACTS:
            path = self.dir / artifact
            try:
                with open(path, encoding="utf-8") as f:
                    self._payloads[artifact] = json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"{artifact}: invalid JSON at line {e.lineno}: {e.msg}")

        if errors:
            raise PreflightError(
                f"Preflight JSON parse errors:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

        # 4. Validate approval status
        approval = self._payloads.get("PREFLIGHT_APPROVAL.json", {})
        status = approval.get("status")
        if status != "approved":
            if status == "rejected":
                reasons = approval.get("rejection_reasons", ["(no reasons given)"])
                raise PreflightError(
                    f"Preflight status is 'rejected'. Reasons:\n"
                    + "\n".join(f"  - {r}" for r in reasons)
                )
            elif status == "insufficient_information":
                missing = approval.get("required_missing_inputs", ["(none listed)"])
                raise PreflightError(
                    f"Preflight status is 'insufficient_information'. Missing inputs:\n"
                    + "\n".join(f"  - {m}" for m in missing)
                )
            else:
                raise PreflightError(
                    f"Preflight status is '{status}' (expected 'approved')"
                )

        # 5. Validate approval_basis is non-empty
        basis = approval.get("approval_basis", [])
        if not basis:
            raise PreflightError(
                "Preflight approved but approval_basis is empty — "
                "approval without stated evidence is invalid"
            )

        # 6. Validate allowed_next_step
        next_step = approval.get("allowed_next_step")
        if next_step != "workspace_generation":
            raise PreflightError(
                f"allowed_next_step is '{next_step}' "
                f"(expected 'workspace_generation')"
            )

        # 7. Validate gates_verified (all must be true)
        gates = approval.get("gates_verified", {})
        failed_gates = [k for k, v in gates.items() if v is not True]
        if failed_gates:
            raise PreflightError(
                f"Preflight gates not all passed: {', '.join(failed_gates)}"
            )

        # 8. Validate CRI fields exist in purpose
        purpose = self._payloads.get("PREFLIGHT_PURPOSE.json", {})
        cri = purpose.get("cri", {})
        required_cri = [
            "target_customer_or_user_class",
            "primary_user_job_to_be_done",
            "business_outcome_hypothesis",
            "monetization_model",
        ]
        missing_cri = [f for f in required_cri if not cri.get(f)]
        if missing_cri:
            errors.append(f"CRI fields missing: {', '.join(missing_cri)}")

        # 9. Validate acceptance criteria exist and meet minimum
        acceptance = self._payloads.get("PREFLIGHT_ACCEPTANCE.json", {})
        criteria = acceptance.get("acceptance_criteria", [])
        computed_min = acceptance.get("computed_minimum", 5)
        if len(criteria) < computed_min:
            errors.append(
                f"Acceptance criteria count ({len(criteria)}) "
                f"below minimum ({computed_min})"
            )

        if errors:
            raise PreflightError(
                f"Preflight content validation failed:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

        self._validated = True
        logger.info(
            "Preflight validated: status=approved, %d criteria, %d decisions, "
            "staging=%s",
            len(criteria),
            len(self._payloads.get("PREFLIGHT_DECISIONS.json", {}).get("decisions", [])),
            self.dir,
        )

    def _require_validated(self) -> None:
        if not self._validated:
            raise PreflightError(
                "Cannot access preflight data before validate_and_load()"
            )

    # ------------------------------------------------------------------
    # Data accessors (safe — raise if not validated)
    # ------------------------------------------------------------------

    @property
    def approval(self) -> Dict[str, Any]:
        self._require_validated()
        return self._payloads["PREFLIGHT_APPROVAL.json"]

    @property
    def purpose(self) -> Dict[str, Any]:
        self._require_validated()
        return self._payloads["PREFLIGHT_PURPOSE.json"]

    @property
    def cri(self) -> Dict[str, Any]:
        self._require_validated()
        return self.purpose.get("cri", {})

    @property
    def purpose_claims(self) -> List[Dict[str, Any]]:
        self._require_validated()
        return self.purpose.get("purpose_claims", [])

    @property
    def absence_map(self) -> Dict[str, Any]:
        self._require_validated()
        return self._payloads["PREFLIGHT_ABSENCE_MAP.json"]

    @property
    def els_risks(self) -> List[Dict[str, Any]]:
        self._require_validated()
        return self.absence_map.get("els_risks", [])

    @property
    def architecture(self) -> Dict[str, Any]:
        self._require_validated()
        return self._payloads["PREFLIGHT_ARCHITECTURE.json"]

    @property
    def minimal_inevitable_set(self) -> List[Dict[str, Any]]:
        self._require_validated()
        raw = (
            self.architecture.get("minimal_inevitable_set")
            or self.architecture.get("components")
            or []
        )
        # Normalize field names (subagent may use 'id' vs 'component_id', etc.)
        normalized = []
        for comp in raw:
            c = dict(comp)
            if "id" in c and "component_id" not in c:
                c["component_id"] = c["id"]
            if "name" in c and "component_name" not in c:
                c["component_name"] = c["name"]
            if "why_inevitable" in c and "justification" not in c:
                c["justification"] = c["why_inevitable"]
            if "failure_mode" in c and "impact_if_removed" not in c:
                c["impact_if_removed"] = c["failure_mode"]
            if "dependencies" in c and "purpose_claims_served" not in c:
                c["purpose_claims_served"] = c.get("dependencies", [])
            if "classification" not in c:
                c["classification"] = "core"
            normalized.append(c)
        return normalized

    @property
    def acceptance(self) -> Dict[str, Any]:
        self._require_validated()
        return self._payloads["PREFLIGHT_ACCEPTANCE.json"]

    @property
    def acceptance_criteria(self) -> List[Dict[str, Any]]:
        self._require_validated()
        raw = self.acceptance.get("acceptance_criteria", [])
        # Normalize field names
        normalized = []
        for ac in raw:
            a = dict(ac)
            if "id" in a and "acceptance_id" not in a:
                a["acceptance_id"] = a["id"]
            if "statement" in a and "criterion_text" not in a:
                a["criterion_text"] = a["statement"]
            if "test_procedure" in a and "pass_condition" not in a:
                a["pass_condition"] = a["test_procedure"]
            if "maps_to_components" in a and "purpose_claim_refs" not in a:
                a["purpose_claim_refs"] = a["maps_to_components"]
            if "verification_method" not in a:
                a["verification_method"] = "manual_binary_check"
            if "fail_condition" not in a:
                a["fail_condition"] = f"Not: {a.get('pass_condition', a.get('criterion_text', ''))}"
            normalized.append(a)
        return normalized

    @property
    def decisions(self) -> List[Dict[str, Any]]:
        self._require_validated()
        raw = self._payloads.get(
            "PREFLIGHT_DECISIONS.json", {}
        ).get("decisions", [])
        # Normalize field names (subagent may use 'id' vs 'decision_id', etc.)
        normalized = []
        for dec in raw:
            d = dict(dec)
            if "id" in d and "decision_id" not in d:
                d["decision_id"] = d["id"]
            if "decision" in d and "decision_statement" not in d:
                d["decision_statement"] = d["decision"]
            if "confidence" in d and "owner_of_decision" not in d:
                d["owner_of_decision"] = d["confidence"]
            if "reversal_trigger" in d and "reversibility_cost_if_wrong" not in d:
                d["reversibility_cost_if_wrong"] = "medium"
                d["reversibility_reason"] = d["reversal_trigger"]
            if "alternatives_rejected" in d and "alternatives_considered" not in d:
                alts = d["alternatives_rejected"]
                if isinstance(alts, list):
                    d["alternatives_considered"] = [
                        {"alternative_text": a.get("alternative", str(a)),
                         "rejection_rationale": a.get("reason", str(a))}
                        if isinstance(a, dict) else
                        {"alternative_text": str(a), "rejection_rationale": "rejected"}
                        for a in alts
                    ]
            normalized.append(d)
        return normalized

    @property
    def non_goals(self) -> List[str]:
        self._require_validated()
        return self.approval.get("non_goals", [])

    @property
    def open_risks(self) -> List[Dict[str, Any]]:
        self._require_validated()
        return self.approval.get("open_risks", [])

    @property
    def workspace_gen_els_risks(self) -> List[Dict[str, Any]]:
        """ELS risks that must be addressed during workspace generation."""
        self._require_validated()
        return [
            r for r in self.els_risks
            if r.get("earliest_cheap_mitigation_stage") == "workspace_gen"
        ]

    # ------------------------------------------------------------------
    # Module generation: derive modules from preflight components
    # ------------------------------------------------------------------

    def generate_modules(self) -> list:
        """Generate ModuleSpec objects from preflight minimal-inevitable-set.

        This REPLACES forge's category-based module resolution when preflight
        exists. Each COMP-NNN from preflight architecture becomes a module.
        Acceptance criteria from preflight are distributed to their matching
        modules. This is the core of "vault 90% + custom 10%".
        """
        self._require_validated()

        # Import ModuleSpec and enums
        try:
            from .forge_engine import ModuleSpec, ModulePriority
        except ImportError:
            from forge_engine import ModuleSpec, ModulePriority

        components = self.minimal_inevitable_set
        if not components:
            return []

        # Map component classification to ModulePriority
        classification_map = {
            "core": ModulePriority.CORE,
            "supporting": ModulePriority.FEATURE,
            "foundation": ModulePriority.FOUNDATION,
            "enhancement": ModulePriority.ENHANCEMENT,
        }

        modules = []
        for i, comp in enumerate(components, 1):
            comp_id = comp.get("component_id", f"COMP-{i:03d}")
            comp_name = comp.get("component_name", f"Component {i}")
            classification = comp.get("classification", "core")
            justification = comp.get("justification", "")
            impact = comp.get("impact_if_removed", "")
            claims = comp.get("purpose_claims_served", [])

            # Derive a slug-style module ID from the component name
            module_id = (
                comp_name.lower()
                .replace(" ", "-")
                .replace("(", "").replace(")", "")
                .replace("/", "-").replace("&", "and")
                .replace("--", "-").strip("-")
            )

            # Find acceptance criteria that reference this component
            module_criteria = []
            comp_name_lower = comp_name.lower()
            for ac in self.acceptance_criteria:
                text = ac.get("criterion_text", "")
                refs = ac.get("purpose_claim_refs", [])
                ac_id = ac.get("acceptance_id", "")
                # Match by component name keywords in criterion text
                if any(word in text.lower() for word in comp_name_lower.split()
                       if len(word) > 3):
                    criterion = f"[PREFLIGHT {ac_id}] {text}"
                    pass_cond = ac.get("pass_condition", "")
                    if pass_cond:
                        criterion += f" (pass: {pass_cond})"
                    module_criteria.append(criterion)

            # Build description from preflight data
            description_parts = [justification]
            if impact:
                description_parts.append(f"If removed: {impact}")
            if claims:
                claims_str = ", ".join(str(c) for c in claims)
                description_parts.append(f"Serves: {claims_str}")
            description = ". ".join(p for p in description_parts if p)

            priority = classification_map.get(classification, ModulePriority.CORE)

            module = ModuleSpec(
                id=module_id,
                name=comp_name,
                priority=priority,
                order=i,
                depends_on=[],  # Will be computed from build_phases
                description=description,
                acceptance_criteria=module_criteria if module_criteria else [
                    f"{comp_name} is set up and verified as functional"
                ],
                customization={
                    "preflight_component_id": comp_id,
                    "preflight_classification": classification,
                },
            )
            modules.append(module)

        # Compute dependencies from preflight build order
        # Parse PREFLIGHT_BUILD_ORDER.md for phase groupings
        build_order_path = self.dir / "PREFLIGHT_BUILD_ORDER.md"
        if build_order_path.exists():
            self._apply_build_order_dependencies(modules, build_order_path)

        # Distribute any acceptance criteria that didn't match a specific module
        unmatched_criteria = []
        matched_ids = set()
        for ac in self.acceptance_criteria:
            ac_id = ac.get("acceptance_id", "")
            text = ac.get("criterion_text", "")
            pass_cond = ac.get("pass_condition", "")
            criterion_str = f"[PREFLIGHT {ac_id}] {text}"
            if pass_cond:
                criterion_str += f" (pass: {pass_cond})"

            found = False
            for m in modules:
                if criterion_str in m.acceptance_criteria:
                    found = True
                    break
            if not found:
                unmatched_criteria.append(criterion_str)

        # Append unmatched criteria to the last module
        if unmatched_criteria and modules:
            modules[-1].acceptance_criteria.extend(unmatched_criteria)

        # Inject ELS workspace_gen risks into first module
        for risk in self.workspace_gen_els_risks:
            risk_text = risk.get("risk", "")
            category = risk.get("category", "")
            if risk_text and modules:
                constraint = f"[ELS {category}] {risk_text}"
                if constraint not in modules[0].acceptance_criteria:
                    modules[0].acceptance_criteria.append(constraint)

        logger.info(
            "Generated %d modules from preflight minimal-inevitable-set "
            "(%d acceptance criteria distributed)",
            len(modules),
            len(self.acceptance_criteria),
        )
        return modules

    def _apply_build_order_dependencies(self, modules: list,
                                         build_order_path: Path) -> None:
        """Parse build order and set module depends_on fields."""
        content = build_order_path.read_text(encoding="utf-8").lower()
        module_by_id = {m.id: m for m in modules}

        # Simple heuristic: modules in later phases depend on
        # the first module in the previous phase
        # Parse "phase N" sections
        import re
        phase_pattern = re.compile(r'phase\s*(\d+)', re.IGNORECASE)
        phases: Dict[int, List[str]] = {}

        current_phase = 0
        for line in content.split("\n"):
            phase_match = phase_pattern.search(line)
            if phase_match:
                current_phase = int(phase_match.group(1))
                if current_phase not in phases:
                    phases[current_phase] = []
            elif current_phase > 0:
                # Check if any module id appears in this line
                for m in modules:
                    if m.id in line or m.name.lower() in line:
                        if m.id not in phases.get(current_phase, []):
                            phases.setdefault(current_phase, []).append(m.id)

        # Set dependencies: each phase depends on all modules in previous phase
        sorted_phases = sorted(phases.keys())
        for i, phase_num in enumerate(sorted_phases):
            if i == 0:
                continue
            prev_phase = sorted_phases[i - 1]
            prev_ids = phases[prev_phase]
            for mid in phases[phase_num]:
                if mid in module_by_id:
                    module_by_id[mid].depends_on = list(prev_ids)

    # ------------------------------------------------------------------
    # Component Enrichment: vault-first, then research-driven
    # ------------------------------------------------------------------

    # Task type classification for vault relevance filtering
    INFRASTRUCTURE_SIGNALS = frozenset([
        "install", "setup", "configure", "create user", "daemon", "service",
        "launchd", "systemd", "homebrew", "brew", "npm install", "deploy",
        "firewall", "permissions", "keychain", "sync", "symlink", "ssh",
        "tailscale", "vpn", "remote", "account", "user isolation",
    ])
    API_DESIGN_SIGNALS = frozenset([
        "endpoint", "route", "handler", "rest api design", "http method",
        "request body", "response body", "status code",
    ])
    FRONTEND_SIGNALS = frozenset([
        "component", "page", "form", "ui", "layout", "responsive", "css",
        "react", "button", "modal", "navigation",
    ])

    def _classify_task_type(self, description: str) -> str:
        """Classify a component's task type from its description."""
        desc_lower = description.lower()
        infra_score = sum(1 for s in self.INFRASTRUCTURE_SIGNALS if s in desc_lower)
        api_score = sum(1 for s in self.API_DESIGN_SIGNALS if s in desc_lower)
        frontend_score = sum(1 for s in self.FRONTEND_SIGNALS if s in desc_lower)

        if infra_score >= api_score and infra_score >= frontend_score:
            return "infrastructure"
        if api_score > frontend_score:
            return "api-design"
        return "frontend"

    def _vault_skill_is_relevant(self, skill_path: Path, task_type: str) -> bool:
        """Check if a vault skill is relevant to the given task type."""
        name = skill_path.stem.lower()

        # Skills that are ALWAYS relevant regardless of task type
        always_relevant = {
            "component-enrichment", "implementation-playbook",
            "contract-authoring", "environment-config", "deploy-checklist",
            "error-handling", "testing-strategy",
        }
        if name in always_relevant:
            return True

        # Infrastructure-specific skills
        infra_skills = {
            "macos-user-isolation", "launchd-daemon", "tailscale-mesh-setup",
            "icloud-workspace-sync",
        }
        if task_type == "infrastructure" and name in infra_skills:
            return True

        # API design skills — only relevant for api-design tasks
        api_only = {
            "api-design", "data-modeling", "database-schema", "pagination",
            "search-filter", "data-fetch",
        }
        if name in api_only:
            return task_type == "api-design"

        # Frontend skills — only relevant for frontend tasks
        frontend_only = {
            "component-creation", "component-arch", "responsive-layout",
            "form-validation", "modal-dialog", "dark-mode", "drag-drop",
            "notification-system", "error-boundary",
        }
        if name in frontend_only:
            return task_type == "frontend"

        # Default: relevant if not in any exclusion set
        return name not in api_only and name not in frontend_only

    def enrich_modules(self, modules: list) -> None:
        """Enrich each module with prescriptive implementation steps.

        Priority order (Ändring A from plan):
        1. Preflight sub_components → implementation steps (primary source)
        2. Preflight acceptance pass_conditions → verification steps
        3. Vault skills matching component's TASK TYPE (not just keywords)
        4. Generic fallback ONLY if 1-3 give < 3 steps

        Vault relevance filtering (Ändring B from plan):
        - Classify each component's task type (infrastructure/api/frontend)
        - Only include vault skills whose domain matches the task type
        - api-design.md does NOT match infrastructure components
        """
        self._require_validated()

        enrichment_data = []

        for module in modules:
            comp_id = module.customization.get("preflight_component_id", module.id)

            # Find the original preflight component
            component = None
            for c in self.minimal_inevitable_set:
                if c.get("component_id") == comp_id:
                    component = c
                    break

            impl_steps = []
            verification = []
            vault_items_used = []
            enrichment_source = "preflight"

            # --- Priority 1: sub_components → implementation steps ---
            if component:
                sub_comps = component.get("sub_components", [])
                for j, sub in enumerate(sub_comps, 1):
                    impl_steps.append(f"{j}. Set up: {sub}")

            # --- Priority 2: acceptance pass_conditions → verification ---
            for ac in module.acceptance_criteria:
                if "(pass:" not in ac:
                    continue
                try:
                    pass_start = ac.index("(pass:") + 6
                    pass_end = ac.rindex(")")
                    pass_text = ac[pass_start:pass_end].strip()
                    if pass_text.startswith("[") and pass_text.endswith("]"):
                        import ast
                        steps = ast.literal_eval(pass_text)
                        if isinstance(steps, list):
                            for s in steps:
                                verification.append(str(s))
                    else:
                        verification.append(pass_text)
                except (ValueError, SyntaxError):
                    pass

            # --- Priority 3: vault skills (ONLY if task-type relevant) ---
            if len(impl_steps) < 3 and select_for_wave:
                task_type = self._classify_task_type(
                    f"{module.name} {module.description}"
                )
                intent = f"{module.name} {module.description}"
                selection = select_for_wave(
                    intent=intent, tier="B", category="", stack="",
                )
                for skill_path_str in selection.get("skills", []):
                    skill_path = Path(skill_path_str)
                    if not skill_path.exists():
                        continue
                    if not self._vault_skill_is_relevant(skill_path, task_type):
                        continue
                    content = skill_path.read_text(encoding="utf-8")
                    vault_items_used.append(skill_path.name)
                    for line in content.split("\n"):
                        stripped = line.strip()
                        if (stripped and stripped[0].isdigit()
                                and ". " in stripped and len(stripped) > 10):
                            impl_steps.append(stripped)
                    if len(impl_steps) >= 8:
                        break
                if vault_items_used:
                    enrichment_source = "vault"

            # --- Priority 4: generic fallback (only if still < 3) ---
            if len(impl_steps) < 3:
                impl_steps.extend([
                    f"1. Research: determine exact steps for {module.name}",
                    f"2. Implement: execute setup following documentation",
                    f"3. Verify: confirm {module.name} works per acceptance criteria",
                ])
                enrichment_source = "fallback"

            # Apply to module
            module.user_flows = impl_steps
            if verification:
                module.user_flows.extend(
                    [f"VERIFY: {v}" for v in verification]
                )

            enrichment_data.append({
                "component_id": comp_id,
                "module_id": module.id,
                "module_name": module.name,
                "implementation_steps": len(impl_steps),
                "verification_steps": len(verification),
                "vault_items_used": vault_items_used,
                "enrichment_source": enrichment_source,
            })

        # Write enrichment artifact
        enrichment_path = self.dir / "PREFLIGHT_ENRICHMENT.json"
        enrichment_path.write_text(
            json.dumps({
                "meta": {
                    "phase_name": "component_enrichment",
                    "project_slug": self.dir.name,
                    "timestamp_utc": datetime.now().isoformat() + "Z",
                },
                "enriched_components": enrichment_data,
                "preflight_primary": sum(
                    1 for e in enrichment_data
                    if e["enrichment_source"] == "preflight"
                ),
                "vault_supplemented": sum(
                    1 for e in enrichment_data
                    if e["enrichment_source"] == "vault"
                ),
                "fallback": sum(
                    1 for e in enrichment_data
                    if e["enrichment_source"] == "fallback"
                ),
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        logger.info(
            "Enriched %d modules: %d from preflight, %d vault-supplemented, %d fallback",
            len(enrichment_data),
            sum(1 for e in enrichment_data if e["enrichment_source"] == "preflight"),
            sum(1 for e in enrichment_data if e["enrichment_source"] == "vault"),
            sum(1 for e in enrichment_data if e["enrichment_source"] == "fallback"),
        )

    # ------------------------------------------------------------------
    # Injection: apply preflight constraints to forge artifacts
    # ------------------------------------------------------------------

    def apply_to_spec(self, spec) -> None:
        """Inject CRI fields into ProjectSpec where they provide
        stronger constraints than onboarding-derived values.

        Does NOT overwrite fields that onboarding already populated
        with user-explicit data. CRI augments, it does not replace.
        """
        self._require_validated()
        cri = self.cri

        # Target audience: CRI is normative (more precise than onboarding)
        if cri.get("target_customer_or_user_class"):
            spec.target_audience = cri["target_customer_or_user_class"]

        # Kill switches → stored as features for downstream visibility
        for trigger in cri.get("kill_switch_triggers", []):
            if isinstance(trigger, dict):
                trigger_text = trigger.get("trigger_text", "")
            elif isinstance(trigger, str):
                trigger_text = trigger
            else:
                trigger_text = str(trigger)
            if trigger_text and trigger_text not in spec.features:
                spec.features.append(f"[KILL_SWITCH] {trigger_text}")

        # Must-have constraints → derivation log
        for constraint in cri.get("must_have_constraints", []):
            if isinstance(constraint, dict):
                text = constraint.get("constraint_text", "")
                source = constraint.get("source", "unknown")
            elif isinstance(constraint, str):
                text = constraint
                source = "preflight"
            else:
                text = str(constraint)
                source = "preflight"
            if text:
                spec.derivation_log.append(
                    f"CRI constraint ({source}): {text}"
                )

        # Monetization → ensures payment module activation
        monetization = cri.get("monetization_model", "unknown")
        if monetization in ("subscription", "transaction_fee", "usage") and not spec.has_payment:
            spec.has_payment = True
            spec.derivation_log.append(
                f"CRI monetization={monetization} → activated payment module"
            )

        logger.info("CRI applied to ProjectSpec: audience=%s, monetization=%s",
                     spec.target_audience, monetization)

    def apply_to_modules(self, modules: list) -> None:
        """Inject preflight acceptance criteria into module specs.

        Preflight criteria (AC-NNN) are PREPENDED to each module's
        acceptance_criteria list. Forge-generated criteria are preserved
        as complementary checks.
        """
        self._require_validated()

        # Build a set of component names from minimal-inevitable set
        component_names = {
            c.get("component_name", "").lower()
            for c in self.minimal_inevitable_set
        }

        for criterion in self.acceptance_criteria:
            ac_id = criterion.get("acceptance_id", "")
            text = criterion.get("criterion_text", "")
            refs = criterion.get("purpose_claim_refs", [])
            pass_cond = criterion.get("pass_condition", "")

            if not text:
                continue

            # Determine which module(s) this criterion applies to.
            # Heuristic: match by purpose_claim_refs keywords against module IDs.
            # If no match, append to the last non-deploy module.
            matched = False
            criterion_text = f"[PREFLIGHT {ac_id}] {text}"
            if pass_cond:
                criterion_text += f" (pass: {pass_cond})"

            for m in modules:
                # Match by component name overlap or keyword in criterion text
                module_keywords = {m.id, m.name.lower()}
                text_lower = text.lower()
                if any(kw in text_lower for kw in module_keywords):
                    if criterion_text not in m.acceptance_criteria:
                        m.acceptance_criteria.insert(0, criterion_text)
                    matched = True
                    break

            if not matched:
                # Append to last non-deploy module as a project-level criterion
                non_deploy = [m for m in modules if m.id != "deploy"]
                if non_deploy:
                    target = non_deploy[-1]
                    if criterion_text not in target.acceptance_criteria:
                        target.acceptance_criteria.insert(0, criterion_text)

        # Inject ELS workspace_gen risks as module constraints
        for risk in self.workspace_gen_els_risks:
            risk_text = risk.get("risk", "")
            category = risk.get("category", "")
            if not risk_text:
                continue

            constraint = f"[ELS {category}] {risk_text}"
            # Add to foundation module if it exists, otherwise first module
            target = None
            for m in modules:
                if m.id == "foundation":
                    target = m
                    break
            if target is None and modules:
                target = modules[0]
            if target is not None and constraint not in target.acceptance_criteria:
                target.acceptance_criteria.append(constraint)

        logger.info(
            "Preflight criteria applied: %d acceptance, %d ELS workspace_gen risks",
            len(self.acceptance_criteria),
            len(self.workspace_gen_els_risks),
        )

    def render_orchestration_decisions(self) -> str:
        """Render preflight decisions as YAML for orchestration.yaml."""
        self._require_validated()
        if not self.decisions:
            return ""

        lines = []
        for dec in self.decisions:
            dec_id = dec.get("decision_id", "unknown")
            statement = dec.get("decision_statement", "")
            owner = dec.get("owner_of_decision", "unknown")
            cost = dec.get("reversibility_cost_if_wrong", "unknown")
            lines.append(
                f'  - id: "{dec_id}"\n'
                f'    statement: "{statement}"\n'
                f'    owner: "{owner}"\n'
                f'    reversibility: "{cost}"\n'
                f'    source: "preflight"'
            )
        return "\n".join(lines)

    def render_project_addendum(self) -> str:
        """Render a preflight section for PROJECT.md."""
        self._require_validated()

        sections = ["## Preflight Architecture (normative)\n"]
        sections.append(
            f"This workspace was generated from approved preflight.\n"
            f"Staging: `{self.dir}`\n"
        )

        # CRI summary
        cri = self.cri
        sections.append("### Commercial Reality Invariants (CRI)\n")
        sections.append(f"- **Target user:** {cri.get('target_customer_or_user_class', 'N/A')}")
        sections.append(f"- **Job to be done:** {cri.get('primary_user_job_to_be_done', 'N/A')}")
        sections.append(f"- **Business outcome:** {cri.get('business_outcome_hypothesis', 'N/A')}")
        sections.append(f"- **Monetization:** {cri.get('monetization_model', 'N/A')}")
        sections.append("")

        # Non-goals
        if self.non_goals:
            sections.append("### Non-Goals (excluded from scope)\n")
            for ng in self.non_goals:
                sections.append(f"- {ng}")
            sections.append("")

        # Open risks
        if self.open_risks:
            sections.append("### Open Risks (acknowledged)\n")
            for risk in self.open_risks:
                risk_text = risk.get("risk_text", str(risk))
                severity = risk.get("severity", "unknown")
                sections.append(f"- [{severity}] {risk_text}")
            sections.append("")

        # Key decisions
        if self.decisions:
            sections.append("### Key Decisions (normative — do not reverse)\n")
            for dec in self.decisions[:10]:  # Cap at 10 to keep readable
                dec_id = dec.get("decision_id", "")
                statement = dec.get("decision_statement", "")
                cost = dec.get("reversibility_cost_if_wrong", "")
                sections.append(f"- **{dec_id}:** {statement} (reversibility: {cost})")
            sections.append("")

        return "\n".join(sections)

    def render_workspace_reference(self) -> str:
        """Render a preflight reference section for WORKSPACE.md."""
        self._require_validated()
        n_criteria = len(self.acceptance_criteria)
        n_decisions = len(self.decisions)
        return (
            f"\n---\n\n"
            f"## Preflight Reference\n\n"
            f"This workspace was generated from approved preflight:\n"
            f"- **Staging:** `{self.dir}`\n"
            f"- **Status:** approved\n"
            f"- **Acceptance criteria:** {n_criteria} (binding — see qa/acceptance.md)\n"
            f"- **Decisions:** {n_decisions} (normative — do not reverse)\n"
            f"- **Approval basis:** {'; '.join(self.approval.get('approval_basis', []))}\n"
        )


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

    def __init__(self, index_catalog: str = None, preflight_dir: str = None):
        self.index_resolver = IndexResolver(index_catalog)
        self.tool_memory_gen = ToolAwareMemoryGenerator()
        self.imperfektum = ImperfektumEngine() if ImperfektumEngine else None
        self.preflight: Optional[PreflightIngestor] = None

        if preflight_dir:
            self.preflight = PreflightIngestor(preflight_dir)
            self.preflight.validate_and_load()  # Fails loudly if invalid

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
        """Copy selected vault files into workspace/vault-selection/ for self-contained execution.

        Workspace must run without access to the Buildr repo. All vault items
        are copied so a fresh agent can load them via workspace-local paths.
        Returns list of all files written.
        """
        import shutil
        selection = self._resolve_wave_selection(blueprint)
        selection_dir = out / "vault-selection"
        selection_dir.mkdir(exist_ok=True)
        repo_root = Path(__file__).resolve().parent.parent

        created: List[str] = []
        local_manifest: Dict[str, List[str]] = {
            g: [] for g in ("skills", "constraints", "routines", "memories")
        }
        local_items: List[str] = []

        for group in ("skills", "constraints", "routines", "memories"):
            group_dir = selection_dir / group
            group_dir.mkdir(exist_ok=True)
            for item in selection.get(group, []):
                item_path = Path(item)
                if not item_path.is_absolute():
                    item_path = repo_root / item_path
                if item_path.exists() and item_path.is_file():
                    dest = group_dir / item_path.name
                    shutil.copy2(item_path, dest)
                    created.append(str(dest))
                    local_path = f"vault-selection/{group}/{item_path.name}"
                    local_manifest[group].append(local_path)
                    local_items.append(local_path)

        # Write manifest with workspace-relative paths (not absolute repo paths)
        selection_path = selection_dir / "001-foundation.json"
        selection_path.write_text(
            json.dumps(local_manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        created.append(str(selection_path))

        # Patch wave file with workspace-local paths
        wave_path = out / "waves" / "001-foundation.md"
        if wave_path.exists():
            wave = wave_path.read_text(encoding="utf-8")
            block = "## Vault Items\nLoad these before executing (copied into vault-selection/):\n"
            if local_items:
                block += "\n".join(f"- {name}" for name in local_items)
            else:
                block += "- (none selected for this wave)"
            if "## Vault Items" in wave and "\n## Steps" in wave:
                before, remainder = wave.split("## Vault Items", 1)
                _, after = remainder.split("\n## Steps", 1)
                wave = before + block + "\n\n## Steps" + after
                wave_path.write_text(wave, encoding="utf-8")

        return created

    def from_blueprint(self, blueprint, output_dir: str) -> List[str]:
        """Build workspace from an existing Forge blueprint.

        If a PreflightIngestor was provided at construction time, its
        approved constraints are injected into the blueprint BEFORE
        scaffold generation — ensuring the workspace is normatively
        aligned with preflight decisions.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        files = []

        # 0. Apply preflight constraints (if preflight was loaded)
        if self.preflight:
            self.preflight.apply_to_spec(blueprint.spec)

            # CRITICAL: Replace forge's category-based modules with
            # preflight-derived modules. Forge modules are generic web
            # templates; preflight modules are project-specific.
            preflight_modules = self.preflight.generate_modules()
            if preflight_modules:
                blueprint.modules = preflight_modules
                # Recompute build phases from new modules
                try:
                    from .forge_engine import ProjectForge
                except ImportError:
                    from forge_engine import ProjectForge
                blueprint.build_phases = ProjectForge._compute_build_phases(
                    blueprint.modules
                )
                # Enrich modules: vault-first, then research flags
                self.preflight.enrich_modules(blueprint.modules)
                logger.info(
                    "Replaced forge modules with %d preflight modules (enriched)",
                    len(preflight_modules),
                )
            else:
                # Fallback: no components in preflight, keep forge modules
                # but still inject preflight criteria
                self.preflight.apply_to_modules(blueprint.modules)

        # 1. Generate Forge scaffold
        if not ScaffoldGenerator:
            raise ImportError("forge_engine.py required for from_blueprint()")

        gen = ScaffoldGenerator()
        # Onboarding ran before blueprint was created — mark complete in state
        files.extend(gen.generate(blueprint, output_dir, onboarding_complete=True))

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

        # 9. Inject preflight references into generated files
        if self.preflight:
            files.extend(self._apply_preflight_to_workspace(out))

        return files

    def _apply_preflight_to_workspace(self, out: Path) -> List[str]:
        """Post-generation: inject preflight references into workspace files.

        Called only when preflight is loaded and validated. Appends
        normative sections to PROJECT.md, WORKSPACE.md, orchestration.yaml,
        and qa/acceptance.md.
        """
        pf = self.preflight
        patched: List[str] = []

        # PROJECT.md: rewrite with preflight data when preflight drives modules
        project_path = out / "PROJECT.md"
        if project_path.exists():
            content = project_path.read_text(encoding="utf-8")

            # If preflight exists, replace forge category/stack/design
            # sections with preflight-accurate architecture data
            if pf.minimal_inevitable_set:
                # Replace misleading forge category/stack/design section
                # Find and replace the "Teknisk Stack" section
                if "## Teknisk Stack" in content and "## Designsystem" in content:
                    before_stack = content.split("## Teknisk Stack")[0]
                    after_design = content.split("## Deriveringslogg")[-1] if "## Deriveringslogg" in content else ""

                    # Build preflight-accurate tech section
                    components = pf.minimal_inevitable_set
                    comp_list = "\n".join(
                        f"| {c.get('component_id', '?')} | {c.get('component_name', '?')} | {c.get('classification', '?')} |"
                        for c in components
                    )
                    tech_section = (
                        f"## Architecture Components (from preflight)\n\n"
                        f"| ID | Component | Classification |\n"
                        f"|---|-----------|----------------|\n"
                        f"{comp_list}\n\n---\n\n"
                    )

                    if after_design:
                        content = before_stack + tech_section + "## Deriveringslogg" + after_design
                    else:
                        content = before_stack + tech_section

                # Fix category line — use "preflight-driven" instead of forge category
                for old_cat in ("booking", "website", "web-app", "e-commerce",
                                "saas", "tool", "api", "custom"):
                    content = content.replace(
                        f"> Kategori: {old_cat}",
                        "> Kategori: preflight-driven"
                    )

                # Remove forge derivation lines that reference wrong category
                cleaned_lines = []
                for line in content.split("\n"):
                    # Keep CRI constraint lines, remove forge category derivations
                    if line.startswith("- category=") or line.startswith("- description mentions"):
                        if "CRI constraint" not in line:
                            continue
                    cleaned_lines.append(line)
                content = "\n".join(cleaned_lines)

            addendum = pf.render_project_addendum()
            if "## Preflight Architecture" not in content:
                content += f"\n---\n\n{addendum}"
            project_path.write_text(content, encoding="utf-8")
            patched.append(str(project_path))

        # WORKSPACE.md: append preflight reference
        workspace_path = out / "WORKSPACE.md"
        if workspace_path.exists():
            content = workspace_path.read_text(encoding="utf-8")
            content += pf.render_workspace_reference()
            workspace_path.write_text(content, encoding="utf-8")
            patched.append(str(workspace_path))

        # orchestration.yaml: inject preflight decisions
        state_path = out / "state" / "orchestration.yaml"
        if state_path.exists():
            content = state_path.read_text(encoding="utf-8")
            decisions_yaml = pf.render_orchestration_decisions()
            if decisions_yaml:
                # Replace empty decisions list with preflight decisions
                content = content.replace(
                    "decisions: []",
                    f"decisions:\n{decisions_yaml}",
                )
            # Add preflight_slug reference
            slug = pf.dir.name
            content += f'\npreflight_slug: "{slug}"\n'
            content += f'preflight_dir: "{pf.dir}"\n'
            state_path.write_text(content, encoding="utf-8")
            patched.append(str(state_path))

        # qa/acceptance.md: prepend preflight acceptance criteria
        acceptance_path = out / "qa" / "acceptance.md"
        if acceptance_path.exists() and pf.acceptance_criteria:
            content = acceptance_path.read_text(encoding="utf-8")
            pf_section = "\n## Preflight Acceptance Criteria (binding)\n\n"
            pf_section += (
                "These criteria were defined during preflight architecture review. "
                "They are **normative** — every criterion must be met.\n\n"
            )
            for criterion in pf.acceptance_criteria:
                ac_id = criterion.get("acceptance_id", "")
                text = criterion.get("criterion_text", "")
                method = criterion.get("verification_method", "")
                pass_cond = criterion.get("pass_condition", "")
                pf_section += f"- [ ] **{ac_id}:** {text}"
                if pass_cond:
                    pf_section += f" (pass: {pass_cond})"
                if method:
                    pf_section += f" [{method}]"
                pf_section += "\n"

            # Insert after the first heading
            if "\n## " in content:
                first_heading_end = content.index("\n## ")
                content = (
                    content[:first_heading_end]
                    + "\n" + pf_section + "\n"
                    + content[first_heading_end:]
                )
            else:
                content += "\n" + pf_section

            acceptance_path.write_text(content, encoding="utf-8")
            patched.append(str(acceptance_path))

        logger.info("Preflight injected into %d workspace files", len(patched))
        return patched

    def from_description(self, description: str, output_dir: str,
                         audience: str = "", feeling: str = "",
                         color: str = "", location: str = "",
                         level: str = "standard") -> List[str]:
        """Build workspace from a plain-text project description.

        If a PreflightIngestor was provided at construction time, CRI
        fields from preflight may augment the onboarding-derived spec
        (see apply_to_spec).
        """
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
    import argparse

    parser = argparse.ArgumentParser(description="Buildr Bridge CLI")
    parser.add_argument("--description", required=True, help="Project description")
    parser.add_argument("--audience", default="", help="Target audience")
    parser.add_argument("--feeling", default="", help="Project feeling/vibe")
    parser.add_argument("--color", default="", help="Color preference")
    parser.add_argument("--location", default="", help="Context location")
    parser.add_argument("--out", default="./workspace", help="Output directory")
    parser.add_argument("--preflight", default=None,
                        help="Path to approved preflight staging directory "
                             "(e.g., v2/.buildr/preflight/my-project)")

    args = parser.parse_args()

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

    # Validate preflight if provided
    if args.preflight:
        print(f"\n  Preflight staging: {args.preflight}")
        try:
            # Validate early so we fail before generating anything
            test_ingestor = PreflightIngestor(args.preflight)
            test_ingestor.validate_and_load()
            print("  Preflight status: APPROVED ✓")
            print(f"  Acceptance criteria: {len(test_ingestor.acceptance_criteria)}")
            print(f"  Decisions: {len(test_ingestor.decisions)}")
        except PreflightError as e:
            print(f"\n  PREFLIGHT GATE FAILED:\n{e}")
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
    builder = WorkspaceBuilder(
        index_catalog=catalog_path,
        preflight_dir=args.preflight,
    )

    files = builder.from_description(
        description=args.description,
        audience=args.audience,
        feeling=args.feeling,
        color=args.color,
        location=args.location,
        output_dir=args.out,
    )

    print(f"\n{'=' * 60}")
    print("  WORKSPACE GENERATED")
    print(f"{'=' * 60}")
    print(f"\n  {len(files)} files in {args.out}/")

    if args.preflight:
        print("\n  Preflight integration:")
        print("    ✦ CRI injected into PROJECT.md")
        print("    ✦ Acceptance criteria injected into qa/acceptance.md")
        print("    ✦ Decisions injected into orchestration.yaml")
        print("    ✦ Preflight reference in WORKSPACE.md")

    print("\n  Next steps:")
    print(f"  1. Point your LLM agent at {args.out}/")
    print("  2. Tell it: 'Read WORKSPACE.md, then follow AGENT.md'")
    print("  3. The project builds itself.")
    print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    main()
