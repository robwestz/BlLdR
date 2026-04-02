"""
End-to-end tests for commercial-grade workspace generation.

Verifies that generated workspaces contain prescriptive content:
- Every module has files_to_create, data_model, user_flows populated (where applicable)
- Every module has a corresponding wave file with imperative steps
- Every module has a corresponding contract with actual interfaces
- orchestration.yaml registers all waves and parallel_phases
- Evaluator format is structured with YAML front-matter
- Acceptance criteria have stable AC-MODULE-NN IDs
- Agent manifest has correct team for category
- Cross-vendor ENTRY-*.md files exist
"""

import os
import shutil
import tempfile
import unittest
import json
import yaml

from engines.forge_engine import (
    ProjectForge, ProjectCategory, TechStack, ProjectBlueprint,
)


def _make_booking_blueprint() -> ProjectBlueprint:
    forge = ProjectForge()
    forge.onboarding.spec.project_name = "Test Booking"
    forge.onboarding.spec.category = ProjectCategory.BOOKING
    forge.onboarding.spec.description = "Booking site for fishing trips"
    forge.onboarding.spec.target_audience = "Tourists"
    forge.onboarding.spec.audience_location = "zanzibar"
    forge.onboarding.spec.feeling = "professional"
    forge.onboarding.spec.color_hint = "blue"
    forge.onboarding.spec.tech_stack = TechStack.NEXTJS
    forge.onboarding.spec.has_payment = True
    forge.onboarding.spec.has_booking = True
    forge.onboarding.spec.needs_database = True
    forge.onboarding.spec.needs_api = True
    forge.onboarding.spec.languages = ["en"]
    forge.onboarding.spec.external_integrations = ["stripe"]
    return forge.create_blueprint()


def _make_webapp_blueprint() -> ProjectBlueprint:
    forge = ProjectForge()
    forge.onboarding.spec.project_name = "Test WebApp"
    forge.onboarding.spec.category = ProjectCategory.WEB_APP
    forge.onboarding.spec.description = "Task management dashboard"
    forge.onboarding.spec.target_audience = "Small teams"
    forge.onboarding.spec.feeling = "minimal"
    forge.onboarding.spec.color_hint = "blue"
    forge.onboarding.spec.tech_stack = TechStack.NEXTJS
    forge.onboarding.spec.has_auth = True
    forge.onboarding.spec.needs_database = True
    forge.onboarding.spec.needs_api = True
    forge.onboarding.spec.languages = ["en"]
    return forge.create_blueprint()


class TestPrescriptiveModules(unittest.TestCase):
    """Test that modules have prescriptive content populated."""

    def test_booking_modules_have_files_to_create(self):
        bp = _make_booking_blueprint()
        core_ids = {"foundation", "design-system", "booking-catalog",
                    "booking-calendar", "payment"}
        for m in bp.modules:
            if m.id in core_ids:
                self.assertGreater(
                    len(m.files_to_create), 0,
                    f"Module {m.id} should have files_to_create populated"
                )

    def test_booking_modules_have_data_models(self):
        bp = _make_booking_blueprint()
        models_expected = {"booking-catalog", "booking-calendar", "payment"}
        for m in bp.modules:
            if m.id in models_expected:
                self.assertGreater(
                    len(m.data_model), 0,
                    f"Module {m.id} should have data_model populated"
                )

    def test_booking_modules_have_user_flows(self):
        bp = _make_booking_blueprint()
        flows_expected = {"booking-catalog", "booking-calendar", "payment"}
        for m in bp.modules:
            if m.id in flows_expected:
                self.assertGreater(
                    len(m.user_flows), 5,
                    f"Module {m.id} should have >= 5 user flow steps"
                )

    def test_booking_modules_have_components(self):
        bp = _make_booking_blueprint()
        comps_expected = {"design-system", "booking-catalog", "booking-calendar", "payment"}
        for m in bp.modules:
            if m.id in comps_expected:
                self.assertGreater(
                    len(m.components), 0,
                    f"Module {m.id} should have components populated"
                )

    def test_webapp_modules_have_prescriptive_data(self):
        bp = _make_webapp_blueprint()
        self.assertTrue(
            any(m.id == "auth" and len(m.files_to_create) > 0 for m in bp.modules),
            "Web-app auth module should have files_to_create"
        )
        self.assertTrue(
            any(m.id == "auth" and len(m.data_model) > 0 for m in bp.modules),
            "Web-app auth module should have data_model"
        )
        self.assertTrue(
            any(m.id == "dashboard" and len(m.files_to_create) > 0 for m in bp.modules),
            "Web-app dashboard module should have files_to_create"
        )


class TestBuildPhases(unittest.TestCase):
    """Test parallel build phase computation."""

    def test_booking_has_parallel_phases(self):
        bp = _make_booking_blueprint()
        self.assertGreater(len(bp.build_phases), 0, "Should have build phases")

    def test_foundation_is_first_phase(self):
        bp = _make_booking_blueprint()
        self.assertIn("foundation", bp.build_phases[0])

    def test_deploy_is_last_phase(self):
        bp = _make_booking_blueprint()
        self.assertIn("deploy", bp.build_phases[-1])

    def test_no_module_missing_from_phases(self):
        bp = _make_booking_blueprint()
        all_ids_in_phases = set()
        for phase in bp.build_phases:
            all_ids_in_phases.update(phase)
        module_ids = {m.id for m in bp.modules}
        self.assertEqual(module_ids, all_ids_in_phases,
                         "All modules should appear in build phases")


class TestWorkspaceGeneration(unittest.TestCase):
    """Test full workspace generation produces expected files."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="buildr_e2e_")
        self.bp = _make_booking_blueprint()
        forge = ProjectForge()
        forge.scaffold_generator.generate(self.bp, self.tmpdir,
                                          onboarding_complete=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_every_module_has_a_wave(self):
        for m in self.bp.modules:
            wave_file = os.path.join(
                self.tmpdir, "waves", f"{m.order:03d}-{m.id}.md"
            )
            self.assertTrue(
                os.path.exists(wave_file),
                f"Wave file missing for module {m.id}: {wave_file}"
            )

    def test_every_module_has_a_contract(self):
        for m in self.bp.modules:
            contract_file = os.path.join(
                self.tmpdir, "contracts", f"{m.id}.md"
            )
            self.assertTrue(
                os.path.exists(contract_file),
                f"Contract file missing for module {m.id}: {contract_file}"
            )

    def test_contracts_have_real_content(self):
        """Contracts should have actual interfaces, not placeholders."""
        contract = os.path.join(self.tmpdir, "contracts", "booking-calendar.md")
        with open(contract, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Booking {", content, "Contract should have Booking entity")
        self.assertIn("Availability {", content, "Contract should have Availability entity")
        self.assertNotIn("shared truth", content, "No placeholder text")

    def test_orchestration_has_all_waves(self):
        state_file = os.path.join(self.tmpdir, "state", "orchestration.yaml")
        with open(state_file, encoding="utf-8") as f:
            state = yaml.safe_load(f)
        self.assertEqual(len(state["waves"]), len(self.bp.modules))

    def test_orchestration_has_parallel_phases(self):
        state_file = os.path.join(self.tmpdir, "state", "orchestration.yaml")
        with open(state_file, encoding="utf-8") as f:
            state = yaml.safe_load(f)
        self.assertIn("parallel_phases", state)
        self.assertGreater(len(state["parallel_phases"]), 0)

    def test_waves_have_imperative_steps(self):
        """Wave files should list concrete file creation steps."""
        wave = os.path.join(self.tmpdir, "waves", "004-booking-calendar.md")
        with open(wave, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Create `src/app/booking/page.tsx`", content)
        self.assertIn("Create `src/components/booking/DatePicker.tsx`", content)

    def test_modules_have_acceptance_ids(self):
        """Module specs should have stable AC-MODULE-NN IDs."""
        mod = os.path.join(self.tmpdir, "modules", "04-booking-calendar.md")
        with open(mod, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("AC-BOOKING_CALENDAR-01", content)

    def test_entry_files_exist(self):
        for name in ("ENTRY-claude.md", "ENTRY-codex.md", "ENTRY-gemini.md"):
            path = os.path.join(self.tmpdir, name)
            self.assertTrue(os.path.exists(path), f"Missing {name}")

    def test_agent_manifest_exists(self):
        manifest = os.path.join(self.tmpdir, "agents", "agent-manifest.json")
        self.assertTrue(os.path.exists(manifest))
        with open(manifest, encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("agents", data)
        agent_names = {a["name"] for a in data["agents"]}
        self.assertIn("orchestrator", agent_names)
        self.assertIn("qa-lead", agent_names)

    def test_evaluator_has_structured_format(self):
        eval_file = os.path.join(self.tmpdir, "qa", "evaluations", "latest.md")
        with open(eval_file, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("verdict:", content)
        self.assertIn("blocker_count:", content)
        self.assertIn("browser_validated:", content)


class TestPreflightIntegration(unittest.TestCase):
    """Test that preflight artifacts are ingested into workspace generation."""

    @staticmethod
    def _create_preflight_staging(tmpdir: str) -> str:
        """Create a minimal but valid set of approved preflight artifacts."""
        staging = os.path.join(tmpdir, "preflight-staging")
        os.makedirs(staging, exist_ok=True)

        purpose = {
            "meta": {"phase_name": "purpose_extraction", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:00:00Z"},
            "purpose_claims": [
                {"claim_id": "PC-001", "claim_text": "Users can book fishing trips online", "falsifiable": True},
                {"claim_id": "PC-002", "claim_text": "Operators receive booking confirmations", "falsifiable": True},
            ],
            "assumptions": [], "exclusions": [],
            "cri": {
                "target_customer_or_user_class": "International tourists visiting Zanzibar",
                "primary_user_job_to_be_done": "Book a fishing trip quickly from mobile",
                "business_outcome_hypothesis": "Increase direct bookings by 40%",
                "monetization_model": "transaction_fee",
                "must_have_constraints": [
                    {"constraint_text": "Must work on slow 3G connections", "source": "user_stated"}
                ],
                "kill_switch_triggers": [
                    {"trigger_text": "Payment integration impossible within 3 weeks",
                     "binary_condition": "stripe_api_unavailable_after_21_days"}
                ],
            },
            "status": "complete",
        }

        absence = {
            "meta": {"phase_name": "absence_mapping", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:01:00Z"},
            "absences": [], "known_unknowns": [],
            "els_risks": [
                {"els_id": "ELS-001", "category": "security_abuse_and_threats",
                 "risk": "No rate limiting on booking API",
                 "why_late_discovery_is_expensive": "Abuse can drain availability",
                 "earliest_cheap_mitigation_stage": "workspace_gen",
                 "residual_open_risk": False},
                {"els_id": "ELS-002", "category": "privacy_and_data_governance",
                 "risk": "Customer PII stored without encryption",
                 "why_late_discovery_is_expensive": "GDPR violation",
                 "earliest_cheap_mitigation_stage": "execution",
                 "residual_open_risk": False},
                {"els_id": "ELS-003", "category": "payments_and_money_movement",
                 "risk": "No webhook verification for Stripe",
                 "why_late_discovery_is_expensive": "Fake payment confirmations",
                 "earliest_cheap_mitigation_stage": "workspace_gen",
                 "residual_open_risk": False},
                {"els_id": "ELS-004", "category": "operational_reliability",
                 "risk": "No health endpoint", "why_late_discovery_is_expensive": "Blind monitoring",
                 "earliest_cheap_mitigation_stage": "execution", "residual_open_risk": False},
                {"els_id": "ELS-005", "category": "accessibility_and_inclusive_design",
                 "risk": "Calendar not keyboard-navigable",
                 "why_late_discovery_is_expensive": "WCAG failure",
                 "earliest_cheap_mitigation_stage": "execution", "residual_open_risk": False},
                {"els_id": "ELS-006", "category": "legal_and_policy_constraints",
                 "risk": "No terms of service", "why_late_discovery_is_expensive": "Legal exposure",
                 "earliest_cheap_mitigation_stage": "execution", "residual_open_risk": False},
            ],
            "els_categories_addressed": [
                {"category": "security_abuse_and_threats", "status": "analyzed"},
                {"category": "privacy_and_data_governance", "status": "analyzed"},
                {"category": "payments_and_money_movement", "status": "analyzed"},
                {"category": "operational_reliability", "status": "analyzed"},
                {"category": "accessibility_and_inclusive_design", "status": "analyzed"},
                {"category": "legal_and_policy_constraints", "status": "analyzed"},
            ],
            "status": "complete",
        }

        architecture = {
            "meta": {"phase_name": "minimal_inevitable_architecture", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:02:00Z"},
            "minimal_inevitable_set": [
                {"component_id": "COMP-001", "component_name": "Web Application Framework",
                 "classification": "core", "justification": "Required for all UI",
                 "purpose_claims_served": ["PC-001"], "impact_if_removed": "No UI"},
                {"component_id": "COMP-002", "component_name": "Booking Engine",
                 "classification": "core", "justification": "Core business logic",
                 "purpose_claims_served": ["PC-001", "PC-002"], "impact_if_removed": "No bookings"},
            ],
            "non_goals": [
                {"non_goal_text": "Native mobile app", "justification": "PWA sufficient for MVP"},
            ],
            "status": "complete",
        }

        acceptance = {
            "meta": {"phase_name": "minimal_inevitable_architecture", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:02:00Z"},
            "acceptance_criteria": [
                {"acceptance_id": "AC-001", "criterion_text": "Booking form submits and returns confirmation ID",
                 "verification_method": "api_response_validation",
                 "purpose_claim_refs": ["PC-001"],
                 "pass_condition": "POST /api/bookings returns 201 with id field",
                 "fail_condition": "Non-201 response or missing id"},
                {"acceptance_id": "AC-002", "criterion_text": "Calendar shows available dates from API",
                 "verification_method": "ui_state_verification",
                 "purpose_claim_refs": ["PC-001"],
                 "pass_condition": "GET /api/availability returns dates; calendar renders them",
                 "fail_condition": "Empty calendar or hardcoded dates"},
                {"acceptance_id": "AC-003", "criterion_text": "Payment completes via Stripe test mode",
                 "verification_method": "api_response_validation",
                 "purpose_claim_refs": ["PC-001"],
                 "pass_condition": "Stripe PaymentIntent succeeds with test card",
                 "fail_condition": "Payment error or no Stripe integration"},
                {"acceptance_id": "AC-004", "criterion_text": "Operator receives email on new booking",
                 "verification_method": "manual_binary_check",
                 "purpose_claim_refs": ["PC-002"],
                 "pass_condition": "Email sent to operator address on booking create",
                 "fail_condition": "No email or wrong recipient"},
                {"acceptance_id": "AC-005", "criterion_text": "Site loads in under 3 seconds on 3G",
                 "verification_method": "performance_threshold",
                 "purpose_claim_refs": ["PC-001"],
                 "pass_condition": "Lighthouse performance score >= 80 on throttled 3G",
                 "fail_condition": "Score < 80 or page not loading"},
            ],
            "non_goals_for_acceptance": ["Native app testing", "Load testing beyond 100 concurrent users"],
            "minimum_criteria_count_formula": "max(5, ceil(purpose_claims_count * 2))",
            "purpose_claims_count": 2,
            "computed_minimum": 5,
        }

        challenge = {
            "meta": {"phase_name": "skeptical_challenge", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:03:00Z"},
            "challenged_components": [
                {"component_id": "COMP-001", "component_name": "Web Application Framework",
                 "challenge_question": "Is a full framework necessary?",
                 "challenge_result": "confirmed"},
            ],
            "challenged_exclusions": [
                {"non_goal_text": "Native mobile app",
                 "challenge_question": "Will tourists expect an app?",
                 "exclusion_safe": True, "risk_if_excluded": "Low — PWA covers use case"},
            ],
            "open_risks": [],
        }

        decisions_data = {
            "meta": {"phase_name": "skeptical_challenge", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:03:00Z"},
            "decisions": [
                {"decision_id": "DEC-001",
                 "decision_statement": "Use Next.js as the web framework",
                 "alternatives_considered": [
                     {"alternative_text": "Astro with islands", "rejection_rationale": "Limited dynamic interactivity for booking flow"},
                     {"alternative_text": "Remix", "rejection_rationale": "Smaller ecosystem for payment integrations"},
                 ],
                 "selected_rationale": "Next.js App Router supports both static pages and dynamic booking flow",
                 "reversibility_cost_if_wrong": "medium",
                 "reversibility_reason": "Framework migration requires rewriting all components",
                 "owner_of_decision": "inferred_high_confidence",
                 "related_purpose_claims": ["PC-001"],
                 "related_component_ids": ["COMP-001"]},
                {"decision_id": "DEC-002",
                 "decision_statement": "Use Stripe for payment processing",
                 "alternatives_considered": [
                     {"alternative_text": "PayPal", "rejection_rationale": "Higher fees for African markets"},
                     {"alternative_text": "M-Pesa direct", "rejection_rationale": "Limited to East Africa; tourists may not have M-Pesa"},
                 ],
                 "selected_rationale": "Stripe has best international coverage and developer experience",
                 "reversibility_cost_if_wrong": "medium",
                 "reversibility_reason": "Payment provider switch requires new integration + testing",
                 "owner_of_decision": "inferred_high_confidence",
                 "related_purpose_claims": ["PC-001"]},
            ],
        }

        approval = {
            "meta": {"phase_name": "approval_synthesis", "project_slug": "test",
                     "timestamp_utc": "2026-04-01T12:04:00Z"},
            "status": "approved",
            "approval_basis": [
                "All CRI fields populated with specific values",
                "5 acceptance criteria meet minimum (max(5, ceil(2*2))=5)",
                "All ELS categories analyzed with mitigations",
                "2 decisions recorded with alternatives and rationale",
            ],
            "rejection_reasons": [],
            "required_missing_inputs": [],
            "open_risks": [],
            "non_goals": ["Native mobile app", "Load testing beyond 100 concurrent users"],
            "minimal_inevitable_set": ["Web Application Framework", "Booking Engine"],
            "allowed_next_step": "workspace_generation",
            "gates_verified": {
                "phase_1_cri_complete": True,
                "phase_2_els_complete": True,
                "phase_2_els_payment_privacy_gate": True,
                "phase_3_acceptance_minimum_met": True,
                "phase_4_decision_gate": True,
                "phase_1_monetization_gate": True,
            },
        }

        # Write all artifacts
        artifacts = {
            "PREFLIGHT_PURPOSE.json": purpose,
            "PREFLIGHT_ABSENCE_MAP.json": absence,
            "PREFLIGHT_ARCHITECTURE.json": architecture,
            "PREFLIGHT_ACCEPTANCE.json": acceptance,
            "PREFLIGHT_CHALLENGE.json": challenge,
            "PREFLIGHT_DECISIONS.json": decisions_data,
            "PREFLIGHT_APPROVAL.json": approval,
        }
        for name, data in artifacts.items():
            with open(os.path.join(staging, name), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        # Write markdown stubs (content not critical for tests, but must exist)
        md_artifacts = [
            "PREFLIGHT_PURPOSE.md", "PREFLIGHT_ABSENCE_MAP.md",
            "PREFLIGHT_ARCHITECTURE.md", "PREFLIGHT_CHALLENGE.md",
            "PREFLIGHT_APPROVAL.md", "PREFLIGHT_DECISIONS.md",
            "PREFLIGHT_ACCEPTANCE.md", "PREFLIGHT_BUILD_ORDER.md",
        ]
        for name in md_artifacts:
            with open(os.path.join(staging, name), "w", encoding="utf-8") as f:
                f.write(f"# {name.replace('.md', '').replace('_', ' ')}\n\nGenerated for testing.\n")

        return staging

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="buildr_pf_e2e_")
        self.staging = self._create_preflight_staging(self.tmpdir)
        self.outdir = os.path.join(self.tmpdir, "workspace")

        from engines.bridge import WorkspaceBuilder
        builder = WorkspaceBuilder(preflight_dir=self.staging)
        builder.from_description(
            description="Booking site for fishing trips in Zanzibar",
            audience="Tourists",
            feeling="professional",
            color="blue",
            location="zanzibar",
            output_dir=self.outdir,
        )

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_project_md_contains_cri(self):
        with open(os.path.join(self.outdir, "PROJECT.md"), encoding="utf-8") as f:
            content = f.read()
        self.assertIn("International tourists visiting Zanzibar", content)
        self.assertIn("transaction_fee", content)
        self.assertIn("Book a fishing trip quickly from mobile", content)

    def test_project_md_contains_non_goals(self):
        with open(os.path.join(self.outdir, "PROJECT.md"), encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Native mobile app", content)

    def test_project_md_contains_decisions(self):
        with open(os.path.join(self.outdir, "PROJECT.md"), encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DEC-001", content)
        self.assertIn("Next.js", content)

    def test_workspace_md_contains_preflight_reference(self):
        with open(os.path.join(self.outdir, "WORKSPACE.md"), encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Preflight Reference", content)
        self.assertIn("approved", content)

    def test_orchestration_has_preflight_decisions(self):
        with open(os.path.join(self.outdir, "state", "orchestration.yaml"),
                  encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DEC-001", content)
        self.assertIn("DEC-002", content)
        self.assertIn("preflight_slug", content)

    def test_acceptance_md_has_preflight_criteria(self):
        with open(os.path.join(self.outdir, "qa", "acceptance.md"),
                  encoding="utf-8") as f:
            content = f.read()
        self.assertIn("AC-001", content)
        self.assertIn("Booking form submits", content)
        self.assertIn("Preflight Acceptance Criteria", content)

    def test_els_workspace_gen_risks_injected(self):
        """ELS risks with stage=workspace_gen should appear in module criteria."""
        # Read all module files and check for ELS constraint
        found = False
        for fname in os.listdir(os.path.join(self.outdir, "modules")):
            with open(os.path.join(self.outdir, "modules", fname), encoding="utf-8") as f:
                content = f.read()
            if "ELS" in content and "rate limiting" in content.lower():
                found = True
                break
        self.assertTrue(found, "ELS workspace_gen risk should be injected into module criteria")

    def test_payment_activated_by_cri_monetization(self):
        """CRI monetization_model=transaction_fee should activate payment module."""
        with open(os.path.join(self.outdir, "state", "orchestration.yaml"),
                  encoding="utf-8") as f:
            content = f.read()
        self.assertIn("payment", content)


class TestPreflightValidation(unittest.TestCase):
    """Test that PreflightIngestor rejects invalid artifacts correctly."""

    def test_rejects_missing_directory(self):
        from engines.bridge import PreflightIngestor, PreflightError
        ingestor = PreflightIngestor("/nonexistent/path")
        with self.assertRaises(PreflightError) as ctx:
            ingestor.validate_and_load()
        self.assertIn("does not exist", str(ctx.exception))

    def test_rejects_rejected_status(self):
        from engines.bridge import PreflightIngestor, PreflightError
        tmpdir = tempfile.mkdtemp()
        try:
            staging = TestPreflightIntegration._create_preflight_staging(tmpdir)
            # Overwrite approval with rejected status
            approval_path = os.path.join(staging, "PREFLIGHT_APPROVAL.json")
            with open(approval_path, encoding="utf-8") as f:
                approval = json.load(f)
            approval["status"] = "rejected"
            approval["rejection_reasons"] = ["Purpose is incoherent"]
            with open(approval_path, "w", encoding="utf-8") as f:
                json.dump(approval, f)

            ingestor = PreflightIngestor(staging)
            with self.assertRaises(PreflightError) as ctx:
                ingestor.validate_and_load()
            self.assertIn("rejected", str(ctx.exception))
            self.assertIn("Purpose is incoherent", str(ctx.exception))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_rejects_empty_approval_basis(self):
        from engines.bridge import PreflightIngestor, PreflightError
        tmpdir = tempfile.mkdtemp()
        try:
            staging = TestPreflightIntegration._create_preflight_staging(tmpdir)
            approval_path = os.path.join(staging, "PREFLIGHT_APPROVAL.json")
            with open(approval_path, encoding="utf-8") as f:
                approval = json.load(f)
            approval["approval_basis"] = []
            with open(approval_path, "w", encoding="utf-8") as f:
                json.dump(approval, f)

            ingestor = PreflightIngestor(staging)
            with self.assertRaises(PreflightError) as ctx:
                ingestor.validate_and_load()
            self.assertIn("approval_basis is empty", str(ctx.exception))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_rejects_missing_artifact(self):
        from engines.bridge import PreflightIngestor, PreflightError
        tmpdir = tempfile.mkdtemp()
        try:
            staging = TestPreflightIntegration._create_preflight_staging(tmpdir)
            # Delete one artifact
            os.remove(os.path.join(staging, "PREFLIGHT_CHALLENGE.json"))
            ingestor = PreflightIngestor(staging)
            with self.assertRaises(PreflightError) as ctx:
                ingestor.validate_and_load()
            self.assertIn("Missing artifact", str(ctx.exception))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_rejects_failed_gate(self):
        from engines.bridge import PreflightIngestor, PreflightError
        tmpdir = tempfile.mkdtemp()
        try:
            staging = TestPreflightIntegration._create_preflight_staging(tmpdir)
            approval_path = os.path.join(staging, "PREFLIGHT_APPROVAL.json")
            with open(approval_path, encoding="utf-8") as f:
                approval = json.load(f)
            approval["gates_verified"]["phase_4_decision_gate"] = False
            with open(approval_path, "w", encoding="utf-8") as f:
                json.dump(approval, f)

            ingestor = PreflightIngestor(staging)
            with self.assertRaises(PreflightError) as ctx:
                ingestor.validate_and_load()
            self.assertIn("phase_4_decision_gate", str(ctx.exception))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
