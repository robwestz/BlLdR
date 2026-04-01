#!/usr/bin/env python3
"""
Preflight artifact validator (v1.5 binary gate).

Validates that a preflight staging directory contains all required artifacts
and that JSON payloads conform to the preflight-handoff schema.

Usage:
    python -m engines.preflight_validate <staging-dir>
    python engines/preflight_validate.py v2/.buildr/preflight/my-project/

Exit codes:
    0 = all validations pass
    1 = one or more validations fail
    2 = missing dependencies or usage error
"""

import json
import sys
from pathlib import Path

SCHEMA_PATH = (
    Path(__file__).parent.parent
    / "v2"
    / "skills"
    / "buildr-workspace-architect"
    / "references"
    / "preflight-handoff.schema.json"
)

REQUIRED_ARTIFACTS = [
    "PREFLIGHT_PURPOSE.md",
    "PREFLIGHT_PURPOSE.json",
    "PREFLIGHT_ABSENCE_MAP.md",
    "PREFLIGHT_ABSENCE_MAP.json",
    "PREFLIGHT_ARCHITECTURE.md",
    "PREFLIGHT_ARCHITECTURE.json",
    "PREFLIGHT_CHALLENGE.md",
    "PREFLIGHT_CHALLENGE.json",
    "PREFLIGHT_APPROVAL.md",
    "PREFLIGHT_APPROVAL.json",
    "PREFLIGHT_BUILD_ORDER.md",
    "PREFLIGHT_DECISIONS.md",
    "PREFLIGHT_DECISIONS.json",
    "PREFLIGHT_ACCEPTANCE.md",
    "PREFLIGHT_ACCEPTANCE.json",
]

REQUIRED_GATES = [
    "phase_1_cri_complete",
    "phase_2_els_complete",
    "phase_2_els_payment_privacy_gate",
    "phase_3_acceptance_minimum_met",
    "phase_4_decision_gate",
    "phase_1_monetization_gate",
]


def validate(staging_dir: str) -> bool:
    staging = Path(staging_dir)
    passed = True

    if not staging.is_dir():
        print(f"FAIL: Staging directory does not exist: {staging}")
        return False

    # --- Artifact existence ---
    for artifact in REQUIRED_ARTIFACTS:
        path = staging / artifact
        if not path.exists():
            print(f"FAIL: Missing artifact: {artifact}")
            passed = False
        else:
            print(f"PASS: {artifact} exists")

    # --- Approval payload checks ---
    approval_path = staging / "PREFLIGHT_APPROVAL.json"
    if approval_path.exists():
        try:
            with open(approval_path, encoding="utf-8") as f:
                approval = json.load(f)

            status = approval.get("status")
            if status == "approved":
                print("PASS: status = approved")
            else:
                print(f"FAIL: status = {status} (expected: approved)")
                passed = False

            basis = approval.get("approval_basis", [])
            if basis:
                print(f"PASS: approval_basis has {len(basis)} entries")
            else:
                print("FAIL: approval_basis is empty")
                passed = False

            next_step = approval.get("allowed_next_step")
            if next_step == "workspace_generation":
                print("PASS: allowed_next_step = workspace_generation")
            else:
                print(f"FAIL: allowed_next_step = {next_step}")
                passed = False

            gates = approval.get("gates_verified", {})
            for gate_name in REQUIRED_GATES:
                if gates.get(gate_name) is True:
                    print(f"PASS: gate {gate_name} = true")
                else:
                    print(f"FAIL: gate {gate_name} = {gates.get(gate_name)}")
                    passed = False

        except json.JSONDecodeError as e:
            print(f"FAIL: PREFLIGHT_APPROVAL.json is not valid JSON: {e}")
            passed = False

    # --- JSON parse check for all JSON artifacts ---
    json_artifacts = [a for a in REQUIRED_ARTIFACTS if a.endswith(".json")]
    for artifact in json_artifacts:
        path = staging / artifact
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                print(f"FAIL: {artifact} is not valid JSON: {e}")
                passed = False

    # --- Schema validation (optional, requires jsonschema) ---
    try:
        import jsonschema  # noqa: F811
    except ImportError:
        print(
            "WARN: jsonschema not installed — skipping schema validation "
            "(pip install jsonschema)"
        )
        return passed

    if not SCHEMA_PATH.exists():
        print(f"WARN: Schema not found at {SCHEMA_PATH} — skipping schema validation")
        return passed

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)

    defs = schema.get("$defs", {})
    artifact_to_def = {
        "PREFLIGHT_PURPOSE.json": "purpose_payload",
        "PREFLIGHT_ABSENCE_MAP.json": "absence_payload",
        "PREFLIGHT_ARCHITECTURE.json": "architecture_payload",
        "PREFLIGHT_ACCEPTANCE.json": "acceptance_payload",
        "PREFLIGHT_CHALLENGE.json": "challenge_payload",
        "PREFLIGHT_DECISIONS.json": "decisions_payload",
        "PREFLIGHT_APPROVAL.json": "approval_payload",
    }

    for artifact, def_name in artifact_to_def.items():
        path = staging / artifact
        if not path.exists():
            continue
        definition = defs.get(def_name)
        if not definition:
            print(f"WARN: No schema definition '{def_name}' for {artifact}")
            continue
        with open(path, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue  # already reported above
        try:
            resolver = jsonschema.RefResolver.from_schema(schema)
            jsonschema.validate(data, definition, resolver=resolver)
            print(f"PASS: {artifact} validates against {def_name}")
        except jsonschema.ValidationError as e:
            print(f"WARN: {artifact} schema issue: {e.message}")
            # Schema validation is advisory in v1.5 — does not block

    return passed


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <staging-directory>")
        print(f"Example: {sys.argv[0]} v2/.buildr/preflight/my-project/")
        sys.exit(2)

    staging_dir = sys.argv[1]
    print(f"Validating preflight artifacts in: {staging_dir}")
    print("=" * 60)

    result = validate(staging_dir)

    print("=" * 60)
    if result:
        print("RESULT: PASS — workspace generation may proceed")
        sys.exit(0)
    else:
        print("RESULT: FAIL — workspace generation blocked")
        sys.exit(1)


if __name__ == "__main__":
    main()
