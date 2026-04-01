"""Tests for engines.preflight_validate (v1.5 preflight staging gate)."""

import json
import tempfile
import unittest
from pathlib import Path

from engines.preflight_validate import REQUIRED_ARTIFACTS, REQUIRED_GATES, validate


def _write_minimal_staging(staging: Path) -> None:
    """Create all required artifact files with content that satisfies validate()."""
    approval = {
        "status": "approved",
        "approval_basis": ["fixture: all gates satisfied for CI"],
        "allowed_next_step": "workspace_generation",
        "gates_verified": {gate: True for gate in REQUIRED_GATES},
    }
    minimal_json = {"fixture": True}
    for name in REQUIRED_ARTIFACTS:
        path = staging / name
        if name.endswith(".md"):
            path.write_text(f"# {name}\n\nfixture\n", encoding="utf-8")
        elif name == "PREFLIGHT_APPROVAL.json":
            path.write_text(json.dumps(approval), encoding="utf-8")
        else:
            path.write_text(json.dumps(minimal_json), encoding="utf-8")


class TestPreflightValidate(unittest.TestCase):
    def test_validate_fails_on_missing_directory(self) -> None:
        self.assertFalse(validate("/nonexistent/preflight/staging-path-xyz"))

    def test_validate_fails_when_artifacts_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp)
            (staging / "PREFLIGHT_PURPOSE.md").write_text("# partial\n", encoding="utf-8")
            self.assertFalse(validate(str(staging)))

    def test_validate_passes_with_full_minimal_staging(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp)
            _write_minimal_staging(staging)
            self.assertTrue(validate(str(staging)))


if __name__ == "__main__":
    unittest.main()
