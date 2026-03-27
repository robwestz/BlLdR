"""Integration tests for the public engines package and WorkspaceBuilder."""

import json
import tempfile
import unittest
from pathlib import Path


class TestEnginesPackage(unittest.TestCase):
    def test_public_package_imports_cleanly(self) -> None:
        import engines

        self.assertTrue(hasattr(engines, "ProjectForge"))
        self.assertTrue(hasattr(engines, "WorkspaceBuilder"))
        self.assertTrue(hasattr(engines, "select_for_wave"))
        self.assertTrue(hasattr(engines, "select_routines"))
        self.assertTrue(hasattr(engines, "select_memories"))


class TestWorkspaceBuilder(unittest.TestCase):
    def test_workspace_builder_emits_canonical_contract(self) -> None:
        import engines

        root = Path(__file__).resolve().parent.parent
        catalog = root / "catalog" / "index.json"

        forge = engines.ProjectForge()
        forge.process_answer(
            "what",
            "Beskriv med en eller två meningar vad du vill bygga.",
            "A simple booking website for fishing trips in Zanzibar",
            ["category"],
        )
        blueprint = forge.create_blueprint()

        with tempfile.TemporaryDirectory() as tmp:
            builder = engines.WorkspaceBuilder(index_catalog=str(catalog))
            written = builder.from_blueprint(blueprint, tmp)
            self.assertTrue(written)

            workspace = Path(tmp) / "WORKSPACE.md"
            self.assertTrue(workspace.is_file())
            content = workspace.read_text(encoding="utf-8")
            self.assertIn("RUN.md", content)
            self.assertIn("state/orchestration.yaml", content)
            self.assertIn("waves/", content)
            self.assertIn("contracts/", content)
            self.assertIn("TOOLS.md", content)


class TestIndexResolver(unittest.TestCase):
    def test_resolve_does_not_mutate_catalog_rows(self) -> None:
        import engines

        root = Path(__file__).resolve().parent.parent
        catalog = root / "catalog" / "index.json"
        resolver = engines.IndexResolver(str(catalog))

        forge = engines.ProjectForge()
        forge.process_answer(
            "what",
            "Beskriv med en eller två meningar vad du vill bygga.",
            "A simple booking website for fishing trips in Zanzibar",
            ["category"],
        )
        blueprint = forge.create_blueprint()

        resolver.resolve(blueprint.spec)

        raw_items = resolver.catalog.get("items", [])
        self.assertTrue(raw_items)
        self.assertFalse(
            any("_selection_reason" in item for item in raw_items),
            "resolver should not mutate catalog items in memory",
        )


if __name__ == "__main__":
    unittest.main()
