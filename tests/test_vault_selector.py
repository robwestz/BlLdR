"""Unit tests for engines.vault_selector — stateless, deterministic selection."""
import importlib.util
import unittest
from pathlib import Path

# Load vault_selector by file path so this suite does not import engines.__init__,
# which pulls in bridge.py (integration layer; may be broken during parallel work).
_ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "_buildrhel_vault_selector_test",
    _ROOT / "engines" / "vault_selector.py",
)
assert _SPEC is not None and _SPEC.loader is not None
_vs = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_vs)

select_constraints = _vs.select_constraints
select_for_wave = _vs.select_for_wave
select_memories = _vs.select_memories
select_routines = _vs.select_routines
select_skills = _vs.select_skills


def _basenames(paths: list[str]) -> set[str]:
    return {Path(p).name for p in paths}


class TestSelectSkills(unittest.TestCase):
    def test_booking_payment_flow_includes_payment_flow(self) -> None:
        out = select_skills("booking payment flow")
        self.assertIn("payment-flow.md", _basenames(out))

    def test_responsive_mobile_layout_includes_responsive_layout(self) -> None:
        out = select_skills("responsive mobile layout")
        self.assertIn("responsive-layout.md", _basenames(out))

    def test_deterministic_repeat_calls(self) -> None:
        intent = "payment api deploy"
        self.assertEqual(select_skills(intent), select_skills(intent))

    def test_upload_keyword_maps_to_file_upload(self) -> None:
        out = select_skills("file upload form")
        self.assertIn("file-upload.md", _basenames(out))

    def test_realtime_keyword_maps_to_realtime_updates(self) -> None:
        out = select_skills("realtime websocket live update")
        self.assertIn("realtime-updates.md", _basenames(out))

    def test_schema_keyword_maps_to_both_data_and_database_skills(self) -> None:
        # "schema" is a multi-skill keyword → should return both files
        out = _basenames(select_skills("schema design"))
        self.assertIn("data-modeling.md", out)
        self.assertIn("database-schema.md", out)

    def test_modal_keyword_maps_to_modal_dialog(self) -> None:
        out = select_skills("modal dialog overlay")
        self.assertIn("modal-dialog.md", _basenames(out))

    def test_environment_keyword_maps_to_environment_config(self) -> None:
        out = select_skills("environment config secret env")
        self.assertIn("environment-config.md", _basenames(out))

    def test_pagination_keyword_maps_to_pagination(self) -> None:
        out = select_skills("pagination infinite scroll")
        self.assertIn("pagination.md", _basenames(out))

    def test_error_boundary_keyword(self) -> None:
        out = select_skills("error boundary crash fallback")
        self.assertIn("error-boundary.md", _basenames(out))


class TestSelectConstraints(unittest.TestCase):
    def test_tier_a_includes_security(self) -> None:
        out = select_constraints("A")
        self.assertIn("security.md", _basenames(out))

    def test_tier_lowercase_normalized(self) -> None:
        self.assertEqual(
            select_constraints("a"),
            select_constraints("A"),
        )

    def test_tier_a_includes_new_architecture_constraints(self) -> None:
        out = _basenames(select_constraints("A"))
        self.assertIn("no-untyped-props.md", out)
        self.assertIn("no-direct-db-in-ui.md", out)

    def test_tier_b_includes_new_runtime_constraints(self) -> None:
        out = _basenames(select_constraints("B"))
        self.assertIn("no-magic-routes.md", out)
        self.assertIn("no-implicit-any.md", out)

    def test_tier_c_includes_async_constraint(self) -> None:
        out = _basenames(select_constraints("C"))
        self.assertIn("no-sync-in-async.md", out)


class TestSelectRoutines(unittest.TestCase):
    def test_tier_c_includes_code_complete(self) -> None:
        out = select_routines("C")
        self.assertIn("code-complete.md", _basenames(out))

    def test_tier_a_includes_dependency_audit_and_pre_commit(self) -> None:
        out = _basenames(select_routines("A"))
        self.assertIn("dependency-audit.md", out)
        self.assertIn("pre-commit.md", out)

    def test_tier_b_includes_security_check(self) -> None:
        out = _basenames(select_routines("B"))
        self.assertIn("security-check.md", out)

    def test_tier_c_includes_performance_check(self) -> None:
        out = _basenames(select_routines("C"))
        self.assertIn("performance-check.md", out)


class TestSelectMemories(unittest.TestCase):
    def test_category_and_stack_includes_universal_category_stack(self) -> None:
        out = select_memories(category="booking", stack="nextjs")
        names = _basenames(out)
        self.assertIn("universal-scars.md", names)
        self.assertIn("universal-insights.md", names)
        self.assertIn("booking.md", names)
        self.assertIn("nextjs.md", names)

    def test_suffixed_memory_naming_convention_found(self) -> None:
        # api-memories.md uses the new {name}-memories.md convention
        out = select_memories(category="api")
        self.assertIn("api-memories.md", _basenames(out))

    def test_suffixed_stack_memory_found(self) -> None:
        # typescript-memories.md uses the new convention
        out = select_memories(stack="typescript")
        self.assertIn("typescript-memories.md", _basenames(out))

    def test_unknown_category_returns_only_universals(self) -> None:
        out = select_memories(category="nonexistent-xyz")
        names = _basenames(out)
        self.assertIn("universal-scars.md", names)
        self.assertIn("universal-insights.md", names)
        self.assertEqual(len(out), 2)


class TestSelectForWave(unittest.TestCase):
    def test_returns_four_list_keys(self) -> None:
        out = select_for_wave(
            intent="checkout flow",
            tier="B",
            category="ecommerce",
            stack="react-vite",
        )
        self.assertEqual(
            set(out.keys()),
            {"skills", "constraints", "routines", "memories"},
        )
        for key in ("skills", "constraints", "routines", "memories"):
            self.assertIsInstance(out[key], list, msg=f"{key} must be a list")

    def test_composes_individual_selectors(self) -> None:
        intent = "mobile payment"
        tier = "C"
        category = "booking"
        stack = "nextjs"
        combined = select_for_wave(intent, tier, category=category, stack=stack)
        self.assertEqual(combined["skills"], select_skills(intent))
        self.assertEqual(combined["constraints"], select_constraints(tier))
        self.assertEqual(combined["routines"], select_routines(tier))
        self.assertEqual(
            combined["memories"],
            select_memories(category, stack),
        )


if __name__ == "__main__":
    unittest.main()
