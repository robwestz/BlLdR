"""
Workspace generation contract tests (Forge / ScaffoldGenerator).

Bridge note (lead): WorkspaceBuilder.from_blueprint() overwrites WORKSPACE.md,
MEMORY.md, and TOOLS.md after ScaffoldGenerator runs. Those overlays should stay
aligned with the canonical contract (RUN.md, state/, waves/, contracts/) —
see engines/bridge.py _render_workspace and _patch_agent.

Import note: forge_engine is loaded by file path so this test stays focused on
Forge scaffold behavior only. Bridge/package import coverage lives in
tests/test_bridge_integration.py.
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "forge_engine_under_test",
    _ROOT / "engines" / "forge_engine.py",
)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
ProjectForge = _mod.ProjectForge


class TestWorkspaceGeneration(unittest.TestCase):
    """Assert Forge scaffold emits the canonical workspace file inventory."""

    REQUIRED_FILES = (
        "WORKSPACE.md",
        "PROJECT.md",
        "SYSTEM.md",
        "MEMORY.md",
        "TOOLS.md",
        "AGENT.md",
        "RUN.md",
        "RUNBOOK.md",
        "state/orchestration.yaml",
        "waves/001-foundation.md",
    )

    REQUIRED_DIRS = ("contracts", "modules", "qa")

    def test_forge_scaffold_includes_canonical_workspace_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            forge = ProjectForge()
            forge.process_answer(
                "what",
                "Beskriv med en eller två meningar vad du vill bygga.",
                "A simple marketing website for a cafe in Stockholm",
                ["category"],
            )
            blueprint = forge.create_blueprint()
            paths = forge.generate_scaffold(blueprint, str(root))

            self.assertTrue(paths, "expected at least one generated path")

            for rel in self.REQUIRED_FILES:
                self.assertTrue(
                    (root / rel).is_file(),
                    f"missing required file: {rel}",
                )

            for d in self.REQUIRED_DIRS:
                self.assertTrue(
                    (root / d).is_dir(),
                    f"missing required directory: {d}/",
                )

            contracts = list((root / "contracts").iterdir())
            self.assertTrue(
                contracts,
                "contracts/ must contain at least one file",
            )

            agent = (root / "AGENT.md").read_text(encoding="utf-8")
            self.assertIn("RUN.md", agent)
            self.assertIn("state/orchestration.yaml", agent)
            self.assertIn("WORKSPACE.md", agent)

            orch = (root / "state" / "orchestration.yaml").read_text(encoding="utf-8")
            self.assertIn("001-foundation", orch)
            self.assertIn("waves:", orch)


if __name__ == "__main__":
    unittest.main()
