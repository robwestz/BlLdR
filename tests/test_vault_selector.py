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


class TestSelectConstraints(unittest.TestCase):
    def test_tier_a_includes_security(self) -> None:
        out = select_constraints("A")
        self.assertIn("security.md", _basenames(out))

    def test_tier_lowercase_normalized(self) -> None:
        self.assertEqual(
            select_constraints("a"),
            select_constraints("A"),
        )


class TestSelectRoutines(unittest.TestCase):
    def test_tier_c_includes_code_complete(self) -> None:
        out = select_routines("C")
        self.assertIn("code-complete.md", _basenames(out))


class TestSelectMemories(unittest.TestCase):
    def test_category_and_stack_includes_universal_category_stack(self) -> None:
        out = select_memories(category="booking", stack="nextjs")
        names = _basenames(out)
        self.assertIn("universal-scars.md", names)
        self.assertIn("universal-insights.md", names)
        self.assertIn("booking.md", names)
        self.assertIn("nextjs.md", names)


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
