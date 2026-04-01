"""
PROJECT FORGE ENGINE v1.0
=========================
"From a conversation to a complete build system."

Takes structured onboarding data and produces a self-contained folder
that any LLM (Claude Code, Codex, Gemini CLI) can autonomously execute
to build the user's project.

ARCHITECTURE (adapted from BACOWR v6.3):
- OnboardingEngine        (guided Q&A → structured project spec)
- ModuleResolver          (spec → activated modules with dependencies)
- DesignDeriver           (feeling + context → concrete design system)
- ScaffoldGenerator       (spec + modules + design → output folder)
- QAGenerator             (modules → binary validation checks)

PIPELINE:
1. CLASSIFY        (user description → project category)
2. PROFILE         (who is it for, who is building it)
3. DISCOVER        (features, behavior, feeling)
4. DERIVE          (technical requirements — NEVER asked, always derived)
5. PLAN            (modules, phases, dependencies)
6. GENERATE        (complete scaffold folder)

DESIGN PRINCIPLES (from BACOWR):
- The user provides ONLY human-language descriptions. NO tech questions.
- The engine DERIVES technical decisions, it does not ask for them.
- Hard constraints + creative freedom = quality output.
- Every decision is traceable (derivation chains).
- 95% of the system is shared across categories. Customization comes
  from onboarding answers, not from different codepaths.
"""

import json
import os
import hashlib
from typing import List, Dict, Optional, Tuple, Set, Any, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
from pathlib import Path


# =============================================================================
# ENUMS
# =============================================================================

class ProjectCategory(str, Enum):
    WEBSITE = "website"
    WEB_APP = "web-app"
    TOOL = "tool"
    E_COMMERCE = "e-commerce"
    BOOKING = "booking"
    SAAS = "saas"
    API = "api"
    CUSTOM = "custom"


class OnboardingLevel(str, Enum):
    EXPRESS = "express"        # 5-7 questions
    STANDARD = "standard"     # 10-15 questions
    PRO = "pro"               # 15-25 questions


class ModulePriority(str, Enum):
    FOUNDATION = "foundation"   # Must be built first
    CORE = "core"               # Essential features
    FEATURE = "feature"         # Category-specific
    ENHANCEMENT = "enhancement" # Nice-to-have
    DEPLOY = "deploy"           # Final step


class TechStack(str, Enum):
    NEXTJS = "nextjs"
    STATIC_HTML = "static-html"
    REACT_VITE = "react-vite"
    PYTHON_FLASK = "python-flask"
    PYTHON_FASTAPI = "python-fastapi"
    ASTRO = "astro"


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class OnboardingAnswer:
    """One answer from the onboarding."""
    phase: int
    question_id: str
    question_text: str
    answer: str
    derived_signals: List[str] = field(default_factory=list)


@dataclass
class ProjectSpec:
    """Complete project specification — derived from onboarding."""
    # Identity
    project_name: str = ""
    category: ProjectCategory = ProjectCategory.CUSTOM
    description: str = ""
    level: OnboardingLevel = OnboardingLevel.STANDARD

    # Who
    owner_type: str = ""           # "business", "personal", "startup"
    target_audience: str = ""
    audience_location: str = ""
    audience_device: str = "mobile-first"
    languages: List[str] = field(default_factory=lambda: ["en"])

    # Feel
    feeling: str = ""              # "professional", "playful", "minimal", etc.
    color_hint: str = ""           # User's color preference in natural language
    existing_brand: bool = False

    # Features (derived from answers)
    features: List[str] = field(default_factory=list)
    has_auth: bool = False
    has_payment: bool = False
    has_booking: bool = False
    has_cms: bool = False
    has_contact: bool = False
    has_search: bool = False

    # Technical (DERIVED, never asked)
    tech_stack: TechStack = TechStack.STATIC_HTML
    needs_database: bool = False
    needs_api: bool = False
    external_integrations: List[str] = field(default_factory=list)

    # Onboarding trace
    answers: List[OnboardingAnswer] = field(default_factory=list)
    derivation_log: List[str] = field(default_factory=list)

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    forge_version: str = "1.0"


@dataclass
class DesignSystem:
    """Concrete design system derived from user's feeling + context."""
    # Colors
    primary: str = "#2563EB"
    primary_light: str = "#3B82F6"
    primary_dark: str = "#1D4ED8"
    secondary: str = "#64748B"
    accent: str = "#F59E0B"
    background: str = "#FFFFFF"
    surface: str = "#F8FAFC"
    text_primary: str = "#0F172A"
    text_secondary: str = "#475569"
    error: str = "#EF4444"
    success: str = "#22C55E"

    # Typography
    font_heading: str = "Inter"
    font_body: str = "Inter"
    font_mono: str = "JetBrains Mono"
    base_size: str = "16px"
    scale_ratio: float = 1.25

    # Spacing
    spacing_unit: str = "0.25rem"
    border_radius: str = "0.5rem"
    max_width: str = "1200px"

    # Component style
    button_style: str = "rounded"    # "rounded", "pill", "square"
    card_style: str = "elevated"     # "elevated", "outlined", "flat"
    input_style: str = "outlined"    # "outlined", "filled", "underlined"

    # Derivation trace
    derived_from: str = ""


@dataclass
class ModuleSpec:
    """Specification for one buildable module."""
    id: str
    name: str
    priority: ModulePriority
    order: int
    depends_on: List[str] = field(default_factory=list)

    # What to build
    description: str = ""
    files_to_create: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)

    # Behavior
    user_flows: List[str] = field(default_factory=list)
    data_model: Dict[str, Any] = field(default_factory=dict)

    # QA
    acceptance_criteria: List[str] = field(default_factory=list)

    # Customization from onboarding
    customization: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProjectBlueprint:
    """Complete blueprint — everything needed to generate the scaffold."""
    spec: ProjectSpec = field(default_factory=ProjectSpec)
    design: DesignSystem = field(default_factory=DesignSystem)
    modules: List[ModuleSpec] = field(default_factory=list)
    build_phases: List[List[str]] = field(default_factory=list)  # module IDs per phase


# =============================================================================
# ONBOARDING ENGINE
# =============================================================================

class OnboardingEngine:
    """
    Guided Q&A that extracts project requirements.

    Maps to BACOWR's pipeline phases 1-3:
    - Phase 1 (classify) = JobSpec loading
    - Phase 2 (profile) = Publisher profiling
    - Phase 3 (discover) = Target fingerprinting

    The key insight: questions are HUMAN, derivations are TECHNICAL.
    The user never sees a technical question.
    """

    # Question banks per category and level
    # Structure: {category: {phase: [(question_id, question_text, signals)]}}
    COMMON_QUESTIONS = {
        1: [  # CLASSIFY
            ("what", "Beskriv med en eller två meningar vad du vill bygga.",
             ["category", "core_feature"]),
        ],
        2: [  # PROFILE
            ("who_for", "Vem är det här till för? Vilka kommer använda det?",
             ["target_audience", "audience_location", "audience_device"]),
            ("existing", "Finns det en befintlig verksamhet eller är det helt nytt?",
             ["owner_type", "existing_brand"]),
            ("brand", "Har du redan färger, logotyp eller en grafisk stil du vill använda?",
             ["color_hint", "existing_brand"]),
        ],
        3: [  # DISCOVER — category-specific questions added by get_questions()
            ("feeling", "Hur vill du att det ska kännas för besökaren? "
             "(t.ex. professionellt, lekfullt, lyxigt, enkelt, tryggt)",
             ["feeling", "design_direction"]),
        ],
    }

    CATEGORY_QUESTIONS = {
        ProjectCategory.WEBSITE: [
            ("pages", "Vilka sidor behövs? (t.ex. Startsida, Om oss, Kontakt, Tjänster)",
             ["features", "page_count"]),
            ("action", "Ska besökare kunna göra något — fylla i formulär, köpa, boka, prenumerera?",
             ["has_contact", "has_payment", "has_booking"]),
        ],
        ProjectCategory.BOOKING: [
            ("book_what", "Vad bokar man? (tid, plats, upplevelse, tjänst)",
             ["booking_type"]),
            ("book_pay", "Ska kunden kunna betala online eller bara boka?",
             ["has_payment"]),
            ("book_flow", "Hur ser en typisk bokning ut — vilka steg går kunden igenom?",
             ["user_flows"]),
            ("book_pricing", "Finns det olika priser, paket, eller säsonger?",
             ["pricing_model"]),
        ],
        ProjectCategory.E_COMMERCE: [
            ("products", "Vad säljs? Ungefär hur många produkter?",
             ["product_type", "catalog_size"]),
            ("payment", "Vilka betalsätt vill du erbjuda? (kort, Swish, faktura)",
             ["payment_methods"]),
            ("shipping", "Behövs frakt/leverans eller är det digitala produkter?",
             ["needs_shipping"]),
        ],
        ProjectCategory.WEB_APP: [
            ("users", "Behöver användare kunna logga in och ha egna konton?",
             ["has_auth"]),
            ("core_action", "Vad är det viktigaste en inloggad användare gör?",
             ["core_feature"]),
            ("data", "Vilken typ av information hanterar systemet?",
             ["data_model"]),
        ],
        ProjectCategory.TOOL: [
            ("tool_input", "Vad matar användaren in?",
             ["input_format"]),
            ("tool_output", "Vad ska komma ut?",
             ["output_format"]),
            ("tool_frequency", "Hur ofta används verktyget — en gång, dagligen, kontinuerligt?",
             ["usage_pattern"]),
        ],
        ProjectCategory.SAAS: [
            ("saas_users", "Ska det finnas olika användarroller? (admin, användare, etc.)",
             ["user_roles"]),
            ("saas_billing", "Ska det vara prenumerationsbaserat? Vilka nivåer?",
             ["pricing_tiers"]),
            ("saas_core", "Beskriv den allra viktigaste funktionen — den som gör att folk betalar.",
             ["core_value_prop"]),
        ],
    }

    def __init__(self):
        self.spec = ProjectSpec()

    def get_questions(self, phase: int, level: OnboardingLevel) -> List[Tuple[str, str, List[str]]]:
        """Get questions for a given phase and level."""
        questions = []

        if phase in self.COMMON_QUESTIONS:
            questions.extend(self.COMMON_QUESTIONS[phase])

        if phase == 3 and self.spec.category in self.CATEGORY_QUESTIONS:
            cat_qs = self.CATEGORY_QUESTIONS[self.spec.category]
            if level == OnboardingLevel.EXPRESS:
                questions.extend(cat_qs[:2])
            elif level == OnboardingLevel.STANDARD:
                questions.extend(cat_qs[:4])
            else:
                questions.extend(cat_qs)

        return questions

    def classify(self, description: str) -> ProjectCategory:
        """Classify project from natural language description."""
        desc = description.lower()

        booking_signals = ["boka", "bokning", "book", "tidsbok", "kalender",
                           "reservation", "appointment", "schedule", "slot"]
        ecommerce_signals = ["sälj", "butik", "shop", "produkt", "köp", "e-handel",
                             "handla", "varukorg", "checkout"]
        webapp_signals = ["dashboard", "inlogg", "login", "konto", "app",
                          "system", "hantera", "manage", "portal"]
        tool_signals = ["verktyg", "tool", "script", "automat", "cli",
                        "konvertera", "bearbeta", "analys"]
        saas_signals = ["saas", "prenumer", "subscription", "multi-tenant",
                        "tier", "plan"]
        api_signals = ["api", "backend", "endpoint", "integration", "webhook"]

        scores = {
            ProjectCategory.BOOKING: sum(1 for s in booking_signals if s in desc),
            ProjectCategory.E_COMMERCE: sum(1 for s in ecommerce_signals if s in desc),
            ProjectCategory.WEB_APP: sum(1 for s in webapp_signals if s in desc),
            ProjectCategory.TOOL: sum(1 for s in tool_signals if s in desc),
            ProjectCategory.SAAS: sum(1 for s in saas_signals if s in desc),
            ProjectCategory.API: sum(1 for s in api_signals if s in desc),
        }

        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best

        # Default: if it mentions "sajt", "sida", "page", "website" → website
        site_signals = ["sajt", "sida", "page", "site", "webb", "landnings",
                        "portfolio", "blogg"]
        if any(s in desc for s in site_signals):
            return ProjectCategory.WEBSITE

        return ProjectCategory.WEBSITE  # safest default

    def process_answer(self, question_id: str, question_text: str,
                       answer: str, signals: List[str]) -> List[str]:
        """Process one answer and derive technical signals."""
        derivations = []
        answer_lower = answer.lower()

        # Store the answer
        self.spec.answers.append(OnboardingAnswer(
            phase=0, question_id=question_id,
            question_text=question_text, answer=answer,
            derived_signals=[]
        ))

        # Phase 1: Classification
        if question_id == "what":
            self.spec.description = answer
            self.spec.category = self.classify(answer)
            derivations.append(f"category={self.spec.category.value}")

            # Derive project name from description
            words = answer.split()[:4]
            self.spec.project_name = "-".join(w.lower() for w in words if len(w) > 2)

        # Phase 2: Profile
        elif question_id == "who_for":
            self.spec.target_audience = answer
            # Derive location/device signals
            location_hints = {
                "zanzibar": ("zanzibar", "mobile-first", ["en", "sw"]),
                "sverige": ("sweden", "responsive", ["sv"]),
                "sweden": ("sweden", "responsive", ["sv", "en"]),
                "global": ("global", "mobile-first", ["en"]),
                "afrika": ("africa", "mobile-first", ["en"]),
                "europa": ("europe", "responsive", ["en"]),
            }
            for hint, (loc, device, langs) in location_hints.items():
                if hint in answer_lower:
                    self.spec.audience_location = loc
                    self.spec.audience_device = device
                    self.spec.languages = langs
                    derivations.append(f"location={loc}, device={device}")

        elif question_id == "existing":
            if any(w in answer_lower for w in ["ny", "new", "start", "första"]):
                self.spec.owner_type = "new"
            else:
                self.spec.owner_type = "existing"
            derivations.append(f"owner_type={self.spec.owner_type}")

        elif question_id == "brand":
            if any(w in answer_lower for w in ["ja", "yes", "finns", "har"]):
                self.spec.existing_brand = True
            color_words = {
                "blå": "blue", "blue": "blue", "röd": "red", "red": "red",
                "grön": "green", "green": "green", "svart": "black", "black": "black",
                "vit": "white", "white": "white", "guld": "gold", "gold": "gold",
                "lila": "purple", "purple": "purple", "orange": "orange",
                "rosa": "pink", "pink": "pink", "turkos": "teal", "teal": "teal",
            }
            for word, color in color_words.items():
                if word in answer_lower:
                    self.spec.color_hint = color
                    derivations.append(f"color_hint={color}")
                    break

        # Phase 3: Features
        elif question_id == "feeling":
            self.spec.feeling = answer

        elif question_id in ("action", "book_pay", "payment"):
            if any(w in answer_lower for w in ["betal", "pay", "köp", "swish",
                                                "kort", "card", "stripe"]):
                self.spec.has_payment = True
                self.spec.features.append("payment")
                derivations.append("has_payment=True")
            if any(w in answer_lower for w in ["boka", "book", "reserv"]):
                self.spec.has_booking = True
                self.spec.features.append("booking")
                derivations.append("has_booking=True")
            if any(w in answer_lower for w in ["formulär", "form", "kontakt", "contact"]):
                self.spec.has_contact = True
                self.spec.features.append("contact")

        elif question_id == "users":
            if any(w in answer_lower for w in ["ja", "yes", "inlogg", "login", "konto"]):
                self.spec.has_auth = True
                self.spec.features.append("auth")
                derivations.append("has_auth=True")

        # Store derivations
        if self.spec.answers:
            self.spec.answers[-1].derived_signals = derivations
        self.spec.derivation_log.extend(derivations)

        return derivations

    def derive_tech_stack(self) -> TechStack:
        """Derive optimal tech stack from project spec. NEVER asked — always derived."""
        if self.spec.category in (ProjectCategory.SAAS, ProjectCategory.WEB_APP):
            self.spec.needs_database = True
            self.spec.needs_api = True
            return TechStack.NEXTJS

        if self.spec.category == ProjectCategory.API:
            self.spec.needs_database = True
            return TechStack.PYTHON_FASTAPI

        if self.spec.category == ProjectCategory.TOOL:
            return TechStack.PYTHON_FLASK

        if self.spec.has_payment or self.spec.has_booking or self.spec.has_auth:
            self.spec.needs_database = True
            self.spec.needs_api = True
            return TechStack.NEXTJS

        if self.spec.category == ProjectCategory.E_COMMERCE:
            self.spec.needs_database = True
            self.spec.needs_api = True
            return TechStack.NEXTJS

        # Simple sites
        return TechStack.STATIC_HTML

    def derive_integrations(self) -> List[str]:
        """Derive needed external integrations."""
        integrations = []

        if self.spec.has_payment:
            if self.spec.audience_location in ("sweden", ""):
                integrations.append("stripe")
            elif self.spec.audience_location in ("zanzibar", "africa"):
                integrations.append("stripe")
                integrations.append("mobile-money")

        if self.spec.has_booking:
            integrations.append("calendar")

        if self.spec.audience_location in ("zanzibar", "africa"):
            integrations.append("whatsapp")

        if self.spec.has_contact:
            integrations.append("email")

        return integrations

    def finalize(self) -> ProjectSpec:
        """Run all derivations and return complete spec."""
        self.spec.tech_stack = self.derive_tech_stack()
        self.spec.external_integrations = self.derive_integrations()
        return self.spec


# =============================================================================
# DESIGN DERIVER
# =============================================================================

class DesignDeriver:
    """
    Derives a concrete design system from feeling + context.

    Maps to BACOWR's publisher voice calibration:
    - User says "professionellt" → specific palette, Inter font, clean spacing
    - User says "lekfullt" → warmer palette, rounded shapes, playful font
    - Context (e.g., Zanzibar fishing) → ocean blues, tropical accents
    """

    FEELING_PALETTES = {
        "professional": {
            "primary": "#1E40AF", "primary_light": "#3B82F6",
            "primary_dark": "#1E3A8A", "accent": "#0EA5E9",
            "font_heading": "Inter", "button_style": "rounded",
        },
        "playful": {
            "primary": "#7C3AED", "primary_light": "#A78BFA",
            "primary_dark": "#5B21B6", "accent": "#F59E0B",
            "font_heading": "Nunito", "button_style": "pill",
            "border_radius": "1rem",
        },
        "luxury": {
            "primary": "#1C1917", "primary_light": "#44403C",
            "primary_dark": "#0C0A09", "accent": "#D4AF37",
            "background": "#FFFBF5", "font_heading": "Playfair Display",
            "button_style": "square", "border_radius": "0",
        },
        "minimal": {
            "primary": "#18181B", "primary_light": "#3F3F46",
            "primary_dark": "#09090B", "accent": "#A1A1AA",
            "font_heading": "Inter", "button_style": "square",
            "border_radius": "0.25rem",
        },
        "warm": {
            "primary": "#B45309", "primary_light": "#D97706",
            "primary_dark": "#92400E", "accent": "#059669",
            "font_heading": "Merriweather",
            "button_style": "rounded",
        },
        "trustworthy": {
            "primary": "#1E40AF", "primary_light": "#2563EB",
            "primary_dark": "#1E3A8A", "accent": "#059669",
            "font_heading": "Source Sans 3",
            "button_style": "rounded",
        },
    }

    COLOR_PALETTES = {
        "blue": {"primary": "#2563EB", "primary_light": "#3B82F6", "primary_dark": "#1D4ED8"},
        "red": {"primary": "#DC2626", "primary_light": "#EF4444", "primary_dark": "#B91C1C"},
        "green": {"primary": "#16A34A", "primary_light": "#22C55E", "primary_dark": "#15803D"},
        "black": {"primary": "#18181B", "primary_light": "#27272A", "primary_dark": "#09090B"},
        "purple": {"primary": "#7C3AED", "primary_light": "#8B5CF6", "primary_dark": "#6D28D9"},
        "gold": {"primary": "#B45309", "primary_light": "#D97706", "primary_dark": "#92400E",
                 "accent": "#D4AF37"},
        "teal": {"primary": "#0D9488", "primary_light": "#14B8A6", "primary_dark": "#0F766E"},
        "orange": {"primary": "#EA580C", "primary_light": "#F97316", "primary_dark": "#C2410C"},
        "pink": {"primary": "#DB2777", "primary_light": "#EC4899", "primary_dark": "#BE185D"},
    }

    CONTEXT_OVERRIDES = {
        "zanzibar": {"accent": "#0EA5E9", "secondary": "#06B6D4"},
        "africa": {"accent": "#D97706"},
        "sweden": {},
    }

    def derive(self, spec: ProjectSpec) -> DesignSystem:
        """Derive complete design system from project spec."""
        ds = DesignSystem()

        # 1. Start with feeling
        feeling_lower = spec.feeling.lower() if spec.feeling else ""
        matched_feeling = None
        for key, palette in self.FEELING_PALETTES.items():
            if key in feeling_lower:
                matched_feeling = key
                for attr, val in palette.items():
                    if hasattr(ds, attr):
                        setattr(ds, attr, val)
                break

        # 2. Override with explicit color
        if spec.color_hint and spec.color_hint in self.COLOR_PALETTES:
            for attr, val in self.COLOR_PALETTES[spec.color_hint].items():
                setattr(ds, attr, val)

        # 3. Apply context overrides
        if spec.audience_location in self.CONTEXT_OVERRIDES:
            for attr, val in self.CONTEXT_OVERRIDES[spec.audience_location].items():
                setattr(ds, attr, val)

        # 4. Mobile-first adjustments
        if spec.audience_device == "mobile-first":
            ds.base_size = "16px"  # Ensure readable on mobile
            ds.spacing_unit = "0.25rem"
            ds.border_radius = ds.border_radius or "0.5rem"

        ds.derived_from = (
            f"feeling='{spec.feeling}', color='{spec.color_hint}', "
            f"location='{spec.audience_location}', matched='{matched_feeling}'"
        )

        return ds


# =============================================================================
# MODULE RESOLVER
# =============================================================================

class ModuleResolver:
    """
    Resolves which modules to build based on project spec.

    Maps to BACOWR's blueprint generation:
    - SectionPlanner → ModulePlanner (sections become modules)
    - Each module has dependencies (connects_to_previous)
    - Acceptance criteria map to QA checks

    SHARED modules (all categories get these):
    - foundation, design-system, deploy

    CATEGORY modules activate based on spec signals.
    """

    # Module definitions: (id, name, priority, depends_on, description, acceptance_criteria)
    SHARED_MODULES = [
        ModuleSpec(
            id="foundation", name="Project Foundation",
            priority=ModulePriority.FOUNDATION, order=1,
            description="Project setup, file structure, dependencies, base config.",
            acceptance_criteria=[
                "Project directory created with correct structure",
                "Package manager initialized",
                "All dependencies installed without errors",
                "Dev server starts without errors",
                "Linting and formatting configured",
            ]
        ),
        ModuleSpec(
            id="design-system", name="Design System",
            priority=ModulePriority.FOUNDATION, order=2,
            depends_on=["foundation"],
            description="Colors, typography, spacing, base components, layout.",
            acceptance_criteria=[
                "CSS variables match design spec exactly",
                "All base components render correctly",
                "Layout responsive at 320px, 768px, 1024px, 1440px",
                "Color contrast meets WCAG AA",
                "Fonts load correctly",
            ]
        ),
    ]

    DEPLOY_MODULE = ModuleSpec(
        id="deploy", name="Deployment",
        priority=ModulePriority.DEPLOY, order=99,
        description="Build, optimize, deploy, domain setup.",
        acceptance_criteria=[
            "Production build completes without errors",
            "All pages/routes load correctly in production mode",
            "Assets optimized (images, CSS, JS)",
            "Meta tags and SEO basics in place",
            "Deployment target configured",
        ]
    )

    CATEGORY_MODULES = {
        ProjectCategory.WEBSITE: [
            ModuleSpec(
                id="pages", name="Pages & Content",
                priority=ModulePriority.CORE, order=3,
                depends_on=["design-system"],
                description="All pages with content, navigation, and responsive layout.",
                acceptance_criteria=[
                    "All specified pages created and accessible",
                    "Navigation works between all pages",
                    "Content matches project description",
                    "All pages responsive",
                    "No placeholder text remaining",
                ]
            ),
            ModuleSpec(
                id="contact-form", name="Contact Form",
                priority=ModulePriority.FEATURE, order=4,
                depends_on=["pages"],
                description="Contact form with validation and submission.",
                acceptance_criteria=[
                    "Form renders with all required fields",
                    "Client-side validation works",
                    "Submission sends data (email/webhook)",
                    "Success/error feedback shown to user",
                ]
            ),
        ],
        ProjectCategory.BOOKING: [
            ModuleSpec(
                id="booking-catalog", name="Services & Packages",
                priority=ModulePriority.CORE, order=3,
                depends_on=["design-system"],
                description="Display of bookable services, packages, and pricing.",
                acceptance_criteria=[
                    "All services/packages displayed with pricing",
                    "Package details expand/show correctly",
                    "Responsive grid/list layout",
                    "Pricing formatted correctly for locale",
                ]
            ),
            ModuleSpec(
                id="booking-calendar", name="Booking Calendar",
                priority=ModulePriority.CORE, order=4,
                depends_on=["booking-catalog"],
                description="Date/time selection, availability display, booking flow.",
                acceptance_criteria=[
                    "Calendar displays available dates",
                    "Unavailable dates clearly marked",
                    "Date selection triggers time slot display",
                    "Booking flow completes: select → confirm → submit",
                    "Confirmation shown after successful booking",
                ]
            ),
            ModuleSpec(
                id="payment", name="Payment Integration",
                priority=ModulePriority.FEATURE, order=5,
                depends_on=["booking-calendar"],
                description="Payment processing for bookings.",
                acceptance_criteria=[
                    "Payment form renders securely",
                    "Test payment completes successfully",
                    "Payment confirmation displayed",
                    "Error handling for failed payments",
                    "Receipt/confirmation email triggered",
                ]
            ),
        ],
        ProjectCategory.WEB_APP: [
            ModuleSpec(
                id="auth", name="Authentication",
                priority=ModulePriority.CORE, order=3,
                depends_on=["design-system"],
                description="User registration, login, session management.",
                acceptance_criteria=[
                    "Registration form with validation",
                    "Login with email/password",
                    "Session persists across page reloads",
                    "Logout clears session",
                    "Protected routes redirect to login",
                ]
            ),
            ModuleSpec(
                id="dashboard", name="User Dashboard",
                priority=ModulePriority.CORE, order=4,
                depends_on=["auth"],
                description="Main user interface after login.",
                acceptance_criteria=[
                    "Dashboard loads after login",
                    "User data displayed correctly",
                    "Navigation between dashboard sections works",
                    "Responsive layout",
                ]
            ),
            ModuleSpec(
                id="data-management", name="Data Management",
                priority=ModulePriority.CORE, order=5,
                depends_on=["dashboard"],
                description="CRUD operations for the core data type.",
                acceptance_criteria=[
                    "Create new items",
                    "Read/list items with pagination",
                    "Update existing items",
                    "Delete items with confirmation",
                    "Data persists across sessions",
                ]
            ),
        ],
        ProjectCategory.E_COMMERCE: [
            ModuleSpec(
                id="product-catalog", name="Product Catalog",
                priority=ModulePriority.CORE, order=3,
                depends_on=["design-system"],
                description="Product listing, categories, search, detail pages.",
                acceptance_criteria=[
                    "Products displayed in grid/list",
                    "Category filtering works",
                    "Product detail page shows all info",
                    "Images load correctly",
                    "Prices formatted for locale",
                ]
            ),
            ModuleSpec(
                id="cart", name="Shopping Cart",
                priority=ModulePriority.CORE, order=4,
                depends_on=["product-catalog"],
                description="Add to cart, quantity, totals, cart persistence.",
                acceptance_criteria=[
                    "Add to cart from product page",
                    "Cart shows correct items and totals",
                    "Quantity adjustable",
                    "Cart persists across page navigation",
                    "Remove items works",
                ]
            ),
            ModuleSpec(
                id="checkout", name="Checkout & Payment",
                priority=ModulePriority.CORE, order=5,
                depends_on=["cart"],
                description="Checkout flow with shipping and payment.",
                acceptance_criteria=[
                    "Checkout form with shipping details",
                    "Order summary displayed",
                    "Payment processing works",
                    "Order confirmation shown",
                    "Confirmation email triggered",
                ]
            ),
        ],
    }

    # Additional modules activated by signals (not category)
    SIGNAL_MODULES = {
        "whatsapp": ModuleSpec(
            id="whatsapp", name="WhatsApp Integration",
            priority=ModulePriority.ENHANCEMENT, order=90,
            depends_on=["design-system"],
            description="WhatsApp contact button/chat widget.",
            acceptance_criteria=[
                "WhatsApp button visible on all pages",
                "Click opens WhatsApp with pre-filled message",
                "Button positioned correctly (mobile: floating, desktop: fixed)",
            ]
        ),
        "multilingual": ModuleSpec(
            id="multilingual", name="Multi-language Support",
            priority=ModulePriority.ENHANCEMENT, order=91,
            depends_on=[],  # Removed "pages" to support non-UI projects
            description="Language switcher and translated content.",
            acceptance_criteria=[
                "Language switcher/selector available",
                "Content switches between languages",
                "Routing or API reflects language selection",
                "Default language matches primary audience",
            ]
        ),
        "seo": ModuleSpec(
            id="seo", name="SEO & Meta Tags",
            priority=ModulePriority.ENHANCEMENT, order=92,
            depends_on=["design-system"],
            description="Meta tags, Open Graph, structured data.",
            acceptance_criteria=[
                "Title and description on all pages",
                "Open Graph tags for social sharing",
                "Favicon and app icons",
                "Sitemap generated",
            ]
        ),
    }

    # =========================================================================
    # PRESCRIPTIVE MODULE DATA (Phase 1: Algorithmic Module Specs)
    # Static dicts — deterministic, instant, testable.
    # =========================================================================

    STACK_FILE_MAPS: Dict[Tuple[str, str], List[str]] = {
        # --- NEXTJS: foundation ---
        ("nextjs", "foundation"): [
            "package.json", "tsconfig.json", "next.config.ts", "tailwind.config.ts",
            "postcss.config.mjs", ".eslintrc.json", ".gitignore", ".env.local",
            "src/app/layout.tsx", "src/app/page.tsx", "src/app/globals.css",
            "src/lib/utils.ts", "public/favicon.ico",
        ],
        ("nextjs", "design-system"): [
            "src/styles/tokens.css",
            "src/components/ui/Button.tsx", "src/components/ui/Card.tsx",
            "src/components/ui/Input.tsx", "src/components/ui/Select.tsx",
            "src/components/ui/Modal.tsx", "src/components/ui/Badge.tsx",
            "src/components/ui/Spinner.tsx",
            "src/components/layout/Header.tsx", "src/components/layout/Footer.tsx",
            "src/components/layout/Container.tsx", "src/components/layout/Navigation.tsx",
        ],
        # --- NEXTJS: booking ---
        ("nextjs", "booking-catalog"): [
            "src/app/services/page.tsx", "src/app/services/[id]/page.tsx",
            "src/components/booking/ServiceCard.tsx",
            "src/components/booking/ServiceGrid.tsx",
            "src/components/booking/PricingTable.tsx",
            "src/lib/services.ts", "src/types/booking.ts", "src/data/services.json",
        ],
        ("nextjs", "booking-calendar"): [
            "src/app/booking/page.tsx", "src/app/booking/[serviceId]/page.tsx",
            "src/components/booking/DatePicker.tsx",
            "src/components/booking/TimeSlotGrid.tsx",
            "src/components/booking/BookingForm.tsx",
            "src/components/booking/BookingSummary.tsx",
            "src/components/booking/AvailabilityIndicator.tsx",
            "src/lib/booking.ts", "src/lib/availability.ts",
            "src/app/api/bookings/route.ts", "src/app/api/availability/route.ts",
        ],
        ("nextjs", "payment"): [
            "src/app/booking/payment/page.tsx",
            "src/app/booking/confirmation/page.tsx",
            "src/components/payment/PaymentForm.tsx",
            "src/components/payment/OrderSummary.tsx",
            "src/components/payment/PaymentStatus.tsx",
            "src/lib/stripe.ts", "src/app/api/payments/route.ts",
            "src/app/api/webhooks/stripe/route.ts",
        ],
        # --- NEXTJS: e-commerce ---
        ("nextjs", "product-catalog"): [
            "src/app/products/page.tsx", "src/app/products/[id]/page.tsx",
            "src/components/products/ProductCard.tsx",
            "src/components/products/ProductGrid.tsx",
            "src/components/products/CategoryFilter.tsx",
            "src/components/products/PriceDisplay.tsx",
            "src/components/products/ImageGallery.tsx",
            "src/lib/products.ts", "src/types/product.ts", "src/data/products.json",
        ],
        ("nextjs", "cart"): [
            "src/app/cart/page.tsx",
            "src/components/cart/CartItem.tsx",
            "src/components/cart/CartSummary.tsx",
            "src/components/cart/CartIcon.tsx",
            "src/components/cart/QuantitySelector.tsx",
            "src/lib/cart.ts", "src/contexts/CartContext.tsx",
        ],
        ("nextjs", "checkout"): [
            "src/app/checkout/page.tsx", "src/app/checkout/confirmation/page.tsx",
            "src/components/checkout/ShippingForm.tsx",
            "src/components/checkout/OrderReview.tsx",
            "src/components/checkout/PaymentSection.tsx",
            "src/lib/checkout.ts", "src/lib/stripe.ts",
            "src/app/api/orders/route.ts", "src/app/api/payments/route.ts",
        ],
        # --- NEXTJS: web-app ---
        ("nextjs", "auth"): [
            "src/app/login/page.tsx", "src/app/register/page.tsx",
            "src/app/forgot-password/page.tsx",
            "src/components/auth/LoginForm.tsx",
            "src/components/auth/RegisterForm.tsx",
            "src/components/auth/AuthGuard.tsx",
            "src/lib/auth.ts", "src/middleware.ts",
            "src/app/api/auth/[...nextauth]/route.ts",
            "src/types/auth.ts",
        ],
        ("nextjs", "dashboard"): [
            "src/app/dashboard/page.tsx", "src/app/dashboard/layout.tsx",
            "src/components/dashboard/Sidebar.tsx",
            "src/components/dashboard/StatsCard.tsx",
            "src/components/dashboard/ActivityFeed.tsx",
            "src/components/dashboard/QuickActions.tsx",
            "src/lib/dashboard.ts",
        ],
        ("nextjs", "data-management"): [
            "src/app/dashboard/items/page.tsx",
            "src/app/dashboard/items/new/page.tsx",
            "src/app/dashboard/items/[id]/page.tsx",
            "src/app/dashboard/items/[id]/edit/page.tsx",
            "src/components/data/DataTable.tsx",
            "src/components/data/DataForm.tsx",
            "src/components/data/DeleteConfirm.tsx",
            "src/components/data/Pagination.tsx",
            "src/lib/data.ts", "src/app/api/items/route.ts",
            "src/app/api/items/[id]/route.ts",
        ],
        # --- NEXTJS: website ---
        ("nextjs", "pages"): [
            "src/app/page.tsx", "src/app/about/page.tsx",
            "src/app/contact/page.tsx",
            "src/components/pages/Hero.tsx",
            "src/components/pages/FeatureSection.tsx",
            "src/components/pages/Testimonials.tsx",
            "src/components/pages/CTA.tsx",
        ],
        ("nextjs", "contact-form"): [
            "src/app/contact/page.tsx",
            "src/components/forms/ContactForm.tsx",
            "src/components/forms/FormField.tsx",
            "src/components/forms/SubmitButton.tsx",
            "src/lib/contact.ts", "src/app/api/contact/route.ts",
        ],
        # --- NEXTJS: shared enhancements ---
        ("nextjs", "whatsapp"): [
            "src/components/widgets/WhatsAppButton.tsx",
            "src/lib/whatsapp.ts",
        ],
        ("nextjs", "multilingual"): [
            "src/lib/i18n.ts", "src/middleware.ts",
            "src/dictionaries/en.json", "src/dictionaries/sw.json",
            "src/components/ui/LanguageSwitcher.tsx",
        ],
        ("nextjs", "seo"): [
            "src/app/sitemap.ts", "src/app/robots.ts",
            "src/lib/seo.ts", "src/components/seo/JsonLd.tsx",
        ],
        ("nextjs", "deploy"): [
            "Dockerfile", ".dockerignore", "vercel.json",
        ],
        # --- STATIC-HTML: foundation ---
        ("static-html", "foundation"): [
            "index.html", "css/reset.css", "css/tokens.css", "css/main.css",
            "js/main.js", ".gitignore", "images/",
        ],
        ("static-html", "design-system"): [
            "css/tokens.css", "css/components.css", "css/layout.css",
            "css/utilities.css",
        ],
        ("static-html", "pages"): [
            "index.html", "about.html", "contact.html",
            "css/pages.css", "js/navigation.js",
        ],
        ("static-html", "contact-form"): [
            "contact.html", "js/form-validation.js", "css/forms.css",
        ],
        ("static-html", "deploy"): [
            "netlify.toml",
        ],
        # --- PYTHON-FASTAPI: foundation ---
        ("python-fastapi", "foundation"): [
            "pyproject.toml", "requirements.txt", ".gitignore", ".env",
            "app/__init__.py", "app/main.py", "app/config.py",
            "app/database.py", "tests/__init__.py", "tests/conftest.py",
            "alembic.ini", "alembic/env.py",
        ],
        ("python-fastapi", "auth"): [
            "app/routers/auth.py", "app/models/user.py",
            "app/schemas/auth.py", "app/services/auth.py",
            "app/dependencies/auth.py", "tests/test_auth.py",
        ],
        ("python-fastapi", "data-management"): [
            "app/routers/items.py", "app/models/item.py",
            "app/schemas/item.py", "app/services/item.py",
            "tests/test_items.py",
        ],
        ("python-fastapi", "deploy"): [
            "Dockerfile", ".dockerignore", "docker-compose.yml",
        ],
    }

    CATEGORY_DATA_MODELS: Dict[Tuple[str, str], Dict[str, Dict[str, str]]] = {
        ("booking", "booking-catalog"): {
            "Service": {
                "id": "string (uuid)", "name": "string", "description": "string",
                "price": "number (cents)", "currency": "string (ISO 4217)",
                "duration_minutes": "integer", "image_url": "string",
                "category": "string", "active": "boolean",
            },
        },
        ("booking", "booking-calendar"): {
            "Booking": {
                "id": "string (uuid)", "service_id": "string (ref: Service.id)",
                "customer_name": "string", "customer_email": "string (email)",
                "customer_phone": "string", "date": "string (ISO 8601 date)",
                "time_slot": "string (HH:MM)", "status": "enum: pending|confirmed|cancelled",
                "notes": "string (optional)", "created_at": "string (ISO 8601)",
            },
            "Availability": {
                "date": "string (ISO 8601 date)", "service_id": "string",
                "slots": "array of {time: string, available: boolean}",
            },
        },
        ("booking", "payment"): {
            "Payment": {
                "id": "string (uuid)", "booking_id": "string (ref: Booking.id)",
                "amount": "number (cents)", "currency": "string",
                "status": "enum: pending|succeeded|failed|refunded",
                "provider_id": "string (Stripe payment intent ID)",
                "created_at": "string (ISO 8601)",
            },
        },
        ("e-commerce", "product-catalog"): {
            "Product": {
                "id": "string (uuid)", "name": "string", "description": "string",
                "price": "number (cents)", "currency": "string (ISO 4217)",
                "images": "array of string (URLs)", "category": "string",
                "stock": "integer", "active": "boolean",
                "attributes": "object (key-value pairs)",
            },
            "Category": {
                "id": "string", "name": "string", "slug": "string",
                "parent_id": "string (optional, ref: Category.id)",
            },
        },
        ("e-commerce", "cart"): {
            "CartItem": {
                "product_id": "string (ref: Product.id)",
                "quantity": "integer (min: 1)", "added_at": "string (ISO 8601)",
            },
            "Cart": {
                "items": "array of CartItem",
                "total_cents": "number (computed)", "currency": "string",
            },
        },
        ("e-commerce", "checkout"): {
            "Order": {
                "id": "string (uuid)", "items": "array of {product_id, quantity, price_at_purchase}",
                "subtotal": "number (cents)", "shipping": "number (cents)",
                "total": "number (cents)", "currency": "string",
                "status": "enum: created|paid|shipped|delivered|cancelled",
                "shipping_address": "object {name, street, city, postal, country}",
                "payment_id": "string", "created_at": "string (ISO 8601)",
            },
        },
        ("web-app", "auth"): {
            "User": {
                "id": "string (uuid)", "email": "string (unique, email)",
                "name": "string", "password_hash": "string (bcrypt)",
                "role": "enum: user|admin", "created_at": "string (ISO 8601)",
                "last_login": "string (ISO 8601, optional)",
            },
            "Session": {
                "id": "string", "user_id": "string (ref: User.id)",
                "expires_at": "string (ISO 8601)",
            },
        },
        ("web-app", "data-management"): {
            "Item": {
                "id": "string (uuid)", "title": "string", "description": "string",
                "status": "enum: draft|active|archived",
                "owner_id": "string (ref: User.id)",
                "created_at": "string (ISO 8601)",
                "updated_at": "string (ISO 8601)",
            },
        },
    }

    DETAILED_USER_FLOWS: Dict[Tuple[str, str], List[str]] = {
        ("booking", "booking-catalog"): [
            "1. User lands on /services page",
            "2. Page loads service list from src/data/services.json (static) or API",
            "3. Services render as cards in a responsive grid (1 col mobile, 2 tablet, 3 desktop)",
            "4. Each card shows: image, name, short description, price, duration, 'Book now' CTA",
            "5. User clicks a card → navigates to /services/[id]",
            "6. Detail page shows: full description, all images, pricing table, availability hint",
            "7. Detail page has prominent 'Book this service' button → links to /booking/[serviceId]",
            "8. User can navigate back to /services via breadcrumb or header nav",
        ],
        ("booking", "booking-calendar"): [
            "1. User arrives at /booking/[serviceId] from service detail page",
            "2. Page displays service name, price, duration at top (read from service data)",
            "3. Calendar component renders current month with day cells",
            "4. Page calls GET /api/availability?serviceId=X&month=YYYY-MM",
            "5. Available dates show as selectable (colored); unavailable dates show as grayed out",
            "6. User clicks an available date → time slot grid appears below calendar",
            "7. Time slots show available/booked status (e.g., 09:00, 10:30, 14:00)",
            "8. User selects a time slot → booking form appears",
            "9. Form fields: name (required), email (required), phone (required), notes (optional)",
            "10. Form validates on blur AND on submit (email format, required fields)",
            "11. User clicks 'Confirm booking' → POST /api/bookings with service_id, date, time, customer data",
            "12. On success → redirect to payment page (if payment enabled) or confirmation page",
            "13. On error → show error message, keep form data, allow retry",
            "14. Confirmation page shows: booking reference, service, date, time, customer info",
        ],
        ("booking", "payment"): [
            "1. User arrives at /booking/payment after booking confirmation",
            "2. Page shows order summary: service name, date, time, price",
            "3. Page calls POST /api/payments to create Stripe PaymentIntent",
            "4. Stripe Elements payment form renders (card number, expiry, CVC)",
            "5. User enters payment details",
            "6. User clicks 'Pay now' → Stripe.js confirms payment",
            "7. On success → POST /api/bookings/[id] to update status to confirmed",
            "8. Redirect to /booking/confirmation with booking reference",
            "9. On failure → show Stripe error message, allow retry",
            "10. Confirmation page shows: receipt summary, booking reference, 'what happens next' text",
        ],
        ("e-commerce", "product-catalog"): [
            "1. User lands on /products page",
            "2. Page loads product list from data source",
            "3. Category filter sidebar renders (desktop: sidebar, mobile: dropdown/sheet)",
            "4. Products render in grid (1 col mobile, 2 tablet, 3-4 desktop)",
            "5. Each card shows: image, name, price, 'Add to cart' button",
            "6. User can filter by category → products filter client-side",
            "7. User clicks product card → navigates to /products/[id]",
            "8. Detail page shows: image gallery, name, description, price, stock status",
            "9. Detail page has 'Add to cart' button with quantity selector",
            "10. If out of stock → button disabled, shows 'Out of stock'",
        ],
        ("e-commerce", "cart"): [
            "1. User clicks 'Add to cart' on product page or product card",
            "2. Cart context updates → cart icon in header shows item count badge",
            "3. User navigates to /cart page",
            "4. Cart shows line items: image thumbnail, name, unit price, quantity selector, line total",
            "5. User adjusts quantity → totals recalculate immediately",
            "6. User clicks remove → item removed with confirmation",
            "7. Cart footer shows: subtotal, estimated shipping, total",
            "8. 'Proceed to checkout' button → navigates to /checkout",
            "9. Empty cart shows message + link back to /products",
            "10. Cart persists in localStorage across page navigations",
        ],
        ("e-commerce", "checkout"): [
            "1. User arrives at /checkout from cart page",
            "2. Page shows order review (items, quantities, prices)",
            "3. Shipping form renders: name, street, city, postal code, country",
            "4. Form validates on blur (required fields, postal code format)",
            "5. After shipping info → payment section appears",
            "6. Stripe Elements renders card input",
            "7. User reviews full order: items + shipping + total",
            "8. User clicks 'Place order' → POST /api/orders + Stripe payment",
            "9. On success → clear cart, redirect to /checkout/confirmation",
            "10. Confirmation shows: order number, items, shipping address, estimated delivery",
            "11. On failure → show error, keep form data, allow retry",
        ],
        ("web-app", "auth"): [
            "1. Unauthenticated user visits any /dashboard/* route",
            "2. Middleware detects no session → redirect to /login",
            "3. Login page shows form: email, password, 'Log in' button, link to /register",
            "4. User enters credentials → POST to auth API",
            "5. On success → session created, redirect to /dashboard",
            "6. On failure → show 'Invalid email or password', keep email field",
            "7. Register page: name, email, password, confirm password",
            "8. Registration validates: email format, password strength (min 8 chars), passwords match",
            "9. On success → auto-login, redirect to /dashboard",
            "10. Forgot password link → /forgot-password → email input → sends reset link",
            "11. Logout button in header → clears session → redirect to /login",
        ],
        ("web-app", "dashboard"): [
            "1. Authenticated user arrives at /dashboard",
            "2. Sidebar renders: navigation links (Dashboard, Items, Settings)",
            "3. Main area shows: welcome message, stats cards (total items, recent activity)",
            "4. Stats cards show key metrics relevant to the user's data",
            "5. Activity feed shows last 10 actions (created, updated, deleted items)",
            "6. Quick actions panel: 'Create new item', 'View all items'",
            "7. Responsive: sidebar collapses to hamburger menu on mobile",
        ],
        ("web-app", "data-management"): [
            "1. User navigates to /dashboard/items from sidebar",
            "2. Data table renders with columns: title, status, created date, actions",
            "3. Pagination: 10 items per page, prev/next controls",
            "4. User clicks 'Create new' → navigates to /dashboard/items/new",
            "5. Form shows: title (required), description (textarea), status (select: draft/active)",
            "6. User fills form → clicks 'Save' → POST /api/items",
            "7. On success → redirect to item detail page /dashboard/items/[id]",
            "8. Detail page shows all fields + 'Edit' and 'Delete' buttons",
            "9. Edit → /dashboard/items/[id]/edit → pre-filled form → PUT /api/items/[id]",
            "10. Delete → confirmation modal → DELETE /api/items/[id] → redirect to list",
            "11. All API errors show user-friendly messages",
        ],
        ("website", "pages"): [
            "1. User lands on / (home page)",
            "2. Hero section: headline, subtext, CTA button",
            "3. Feature section: 3-4 feature cards in grid",
            "4. Testimonials section: 2-3 testimonial cards",
            "5. CTA section: final call-to-action with button",
            "6. Header: logo + nav links (Home, About, Contact)",
            "7. Footer: copyright, links, social icons",
            "8. /about page: company story, team, mission",
            "9. All pages share consistent header/footer/navigation",
            "10. Navigation highlights current page",
        ],
        ("website", "contact-form"): [
            "1. User navigates to /contact",
            "2. Form renders: name (required), email (required), subject, message (required)",
            "3. Validation on blur: email format, required fields",
            "4. User clicks 'Send' → POST /api/contact",
            "5. On success → show success message, clear form",
            "6. On failure → show error, keep form data",
            "7. Button shows loading state during submission",
        ],
    }

    MODULE_COMPONENTS: Dict[Tuple[str, str], List[str]] = {
        ("nextjs", "design-system"): [
            "Button (variant: primary|secondary|outline, size: sm|md|lg, disabled, loading)",
            "Card (variant: elevated|outlined|flat, padding, children)",
            "Input (type, label, error, placeholder, required)",
            "Select (options[], label, error, placeholder)",
            "Modal (open, onClose, title, children, footer)",
            "Badge (variant: default|success|warning|error, children)",
            "Spinner (size: sm|md|lg)",
            "Header (navigation items, logo, auth state)",
            "Footer (links, copyright)",
            "Container (maxWidth, padding, children)",
            "Navigation (items[], activeItem, mobile hamburger menu)",
        ],
        ("nextjs", "booking-catalog"): [
            "ServiceCard (service: Service, onBookClick)",
            "ServiceGrid (services: Service[], loading)",
            "PricingTable (service: Service, currency: string)",
        ],
        ("nextjs", "booking-calendar"): [
            "DatePicker (availableDates[], selectedDate, onSelect, month, onMonthChange)",
            "TimeSlotGrid (slots: Slot[], selectedSlot, onSelect)",
            "BookingForm (serviceId, date, timeSlot, onSubmit, loading)",
            "BookingSummary (service, date, time, customer)",
            "AvailabilityIndicator (status: available|limited|unavailable)",
        ],
        ("nextjs", "payment"): [
            "PaymentForm (clientSecret, onSuccess, onError)",
            "OrderSummary (booking: Booking, service: Service)",
            "PaymentStatus (status: pending|succeeded|failed)",
        ],
        ("nextjs", "product-catalog"): [
            "ProductCard (product: Product, onAddToCart)",
            "ProductGrid (products: Product[], loading)",
            "CategoryFilter (categories: Category[], selected, onChange)",
            "PriceDisplay (amount: number, currency: string)",
            "ImageGallery (images: string[], alt: string)",
        ],
        ("nextjs", "cart"): [
            "CartItem (item: CartItem, product: Product, onUpdateQuantity, onRemove)",
            "CartSummary (cart: Cart)",
            "CartIcon (itemCount: number, onClick)",
            "QuantitySelector (value: number, min, max, onChange)",
        ],
        ("nextjs", "checkout"): [
            "ShippingForm (onSubmit, initialValues)",
            "OrderReview (items: CartItem[], products: Product[])",
            "PaymentSection (clientSecret, onSuccess)",
        ],
        ("nextjs", "auth"): [
            "LoginForm (onSubmit, loading, error)",
            "RegisterForm (onSubmit, loading, error)",
            "AuthGuard (children, fallback: redirect path)",
        ],
        ("nextjs", "dashboard"): [
            "Sidebar (navItems[], activeItem, collapsed)",
            "StatsCard (title, value, change, icon)",
            "ActivityFeed (activities: Activity[])",
            "QuickActions (actions: Action[])",
        ],
        ("nextjs", "data-management"): [
            "DataTable (columns[], data[], onRowClick, pagination)",
            "DataForm (fields[], initialValues, onSubmit, loading)",
            "DeleteConfirm (itemName, onConfirm, onCancel)",
            "Pagination (currentPage, totalPages, onPageChange)",
        ],
    }

    def resolve(self, spec: ProjectSpec) -> List[ModuleSpec]:
        """Resolve all modules for the project."""
        modules = []

        # 1. Shared modules (always)
        for m in self.SHARED_MODULES:
            modules.append(self._customize(m, spec))

        # 2. Category modules
        if spec.category in self.CATEGORY_MODULES:
            for m in self.CATEGORY_MODULES[spec.category]:
                # Skip modules that aren't needed
                if m.id == "contact-form" and not spec.has_contact:
                    continue
                if m.id == "payment" and not spec.has_payment:
                    continue
                modules.append(self._customize(m, spec))

        # 3. Signal-activated modules
        if "whatsapp" in spec.external_integrations:
            modules.append(self.SIGNAL_MODULES["whatsapp"])
        if len(spec.languages) > 1:
            from dataclasses import asdict as _asdict
            ml = ModuleSpec(**_asdict(self.SIGNAL_MODULES["multilingual"]))
            existing_ids = {m.id for m in modules}
            # Depend on "pages" for websites, "design-system" for all others
            ml.depends_on = (
                ["pages"] if "pages" in existing_ids
                else ["design-system"] if "design-system" in existing_ids
                else []
            )
            modules.append(self._customize(ml, spec))

        # SEO module for all websites and booking sites
        if spec.category in (ProjectCategory.WEBSITE, ProjectCategory.BOOKING,
                             ProjectCategory.E_COMMERCE):
            modules.append(self.SIGNAL_MODULES["seo"])

        # 4. Deploy (always last)
        deploy = ModuleSpec(**asdict(self.DEPLOY_MODULE))
        deploy.depends_on = [m.id for m in modules]  # depends on everything
        modules.append(deploy)

        # Sort by order
        modules.sort(key=lambda m: m.order)

        # Re-number
        for i, m in enumerate(modules, 1):
            m.order = i

        return modules

    def _customize(self, module: ModuleSpec, spec: ProjectSpec) -> ModuleSpec:
        """Apply project-specific customization to a module."""
        m = ModuleSpec(**asdict(module))

        # Add project-specific context to description
        if spec.description:
            m.customization["project_context"] = spec.description
        if spec.target_audience:
            m.customization["target_audience"] = spec.target_audience
        if spec.audience_location:
            m.customization["locale"] = spec.audience_location

        # --- Prescriptive field population from static dicts ---
        stack_key = spec.tech_stack.value if hasattr(spec.tech_stack, "value") else str(spec.tech_stack)
        cat_key = spec.category.value if hasattr(spec.category, "value") else str(spec.category)

        # Files to create
        file_key = (stack_key, m.id)
        if file_key in self.STACK_FILE_MAPS:
            m.files_to_create = list(self.STACK_FILE_MAPS[file_key])

        # Data model
        model_key = (cat_key, m.id)
        if model_key in self.CATEGORY_DATA_MODELS:
            m.data_model = dict(self.CATEGORY_DATA_MODELS[model_key])

        # User flows
        flow_key = (cat_key, m.id)
        if flow_key in self.DETAILED_USER_FLOWS:
            m.user_flows = list(self.DETAILED_USER_FLOWS[flow_key])

        # Components
        comp_key = (stack_key, m.id)
        if comp_key in self.MODULE_COMPONENTS:
            m.components = list(self.MODULE_COMPONENTS[comp_key])

        return m


# =============================================================================
# SCAFFOLD GENERATOR
# =============================================================================

class ScaffoldGenerator:
    """
    Produces the complete output folder.

    Maps to BACOWR's AgentPromptRenderer — but instead of one prompt,
    it produces an entire folder of files that constitute a self-contained
    build system.
    """

    @staticmethod
    def _repo_root() -> Path:
        return Path(__file__).resolve().parent.parent

    @classmethod
    def _templates_dir(cls) -> Path:
        return cls._repo_root() / "templates"

    @classmethod
    def _read_template(cls, relative_path: str) -> Optional[str]:
        path = cls._templates_dir() / relative_path.replace("/", os.sep)
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8")

    @staticmethod
    def _fill_placeholders(template: str, mapping: Dict[str, str]) -> str:
        result = template
        for key, val in mapping.items():
            result = result.replace("{{" + key + "}}", val)
        return result

    def generate(self, blueprint: ProjectBlueprint, output_dir: str,
                 onboarding_complete: bool = False) -> List[str]:
        """Generate all scaffold files. Returns list of created file paths.

        Pass onboarding_complete=True when generating via the bridge (onboarding
        was already run to produce the blueprint). False for Forge-only scaffolds
        where the agent should run onboarding/prompt.md before building.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "modules").mkdir(exist_ok=True)
        (out / "qa").mkdir(exist_ok=True)
        (out / "qa" / "evaluations").mkdir(parents=True, exist_ok=True)
        (out / "state").mkdir(exist_ok=True)
        (out / "waves").mkdir(exist_ok=True)
        (out / "contracts").mkdir(exist_ok=True)

        created = []

        # 1. PROJECT.md
        created.append(self._write(out / "PROJECT.md",
                                   self._render_project(blueprint)))

        # 2. SYSTEM.md
        created.append(self._write(out / "SYSTEM.md",
                                   self._render_system(blueprint)))

        # 3. RUNBOOK.md (supplemental per-module detail; RUN.md is canonical)
        created.append(self._write(out / "RUNBOOK.md",
                                   self._render_runbook(blueprint)))

        # 4. Orchestration state (registers ALL waves)
        created.append(self._write(
            out / "state" / "orchestration.yaml",
            self._render_orchestration_yaml(blueprint, onboarding_complete),
        ))

        # 4b. Generate one wave + one contract PER MODULE
        for module in blueprint.modules:
            wave_num = module.order
            wave_id = f"{wave_num:03d}-{module.id}"
            created.append(self._write(
                out / "waves" / f"{wave_id}.md",
                self._render_wave_for_module(module, blueprint, wave_num),
            ))
            created.append(self._write(
                out / "contracts" / f"{module.id}.md",
                self._render_contract_for_module(module, blueprint),
            ))

        # 5. WORKSPACE / MEMORY / TOOLS / RUN (bridge may overwrite the first three)
        created.append(self._write(
            out / "WORKSPACE.md",
            self._render_workspace_md(blueprint),
        ))
        created.append(self._write(
            out / "MEMORY.md",
            self._render_memory_stub(blueprint),
        ))
        created.append(self._write(
            out / "TOOLS.md",
            self._render_tools_stub(blueprint),
        ))
        created.append(self._write(
            out / "RUN.md",
            self._render_run_md(blueprint),
        ))

        # 6. Orchestration protocol + agent role files
        claude_template = self._read_template("CLAUDE.md")
        if claude_template:
            created.append(self._write(out / "CLAUDE.md", claude_template))

        created.append(self._write(out / "AGENT.md",
                                   self._render_agent(blueprint)))
        created.append(self._write(out / "EVALUATOR.md",
                                   self._render_evaluator(blueprint)))
        created.append(self._write(
            out / "qa" / "evaluations" / "latest.md",
            self._render_evaluation_stub(blueprint),
        ))

        # Copy onboarding prompt if it exists (for RUN.md step 6)
        repo_root = Path(__file__).resolve().parent.parent
        onboarding_src = repo_root / "templates" / "onboarding" / "prompt.md"
        if onboarding_src.exists():
            (out / "onboarding").mkdir(exist_ok=True)
            import shutil
            shutil.copy2(onboarding_src, out / "onboarding" / "prompt.md")
            created.append(str(out / "onboarding" / "prompt.md"))

        # 7. Module files
        for module in blueprint.modules:
            fname = f"{module.order:02d}-{module.id}.md"
            created.append(self._write(
                out / "modules" / fname,
                self._render_module(module, blueprint)
            ))

        # 8. QA files
        created.append(self._write(out / "qa" / "checklist.md",
                                   self._render_checklist(blueprint)))
        created.append(self._write(out / "qa" / "acceptance.md",
                                   self._render_acceptance(blueprint)))

        # 8b. Quality gates (3-phase: concept → implementation → delivery)
        gates_template = self._read_template("qa/gates.md")
        if gates_template:
            created.append(self._write(out / "qa" / "gates.md", gates_template))

        # 9. Spec dump (for reproducibility)
        created.append(self._write(
            out / "spec.json",
            json.dumps(asdict(blueprint.spec), indent=2, ensure_ascii=False,
                       default=str)
        ))

        # 10. Agent team (derived from category + modules)
        created.extend(self._generate_agent_team(out, blueprint))

        return created

    # -----------------------------------------------------------------
    # AGENT TEAM GENERATION
    # -----------------------------------------------------------------

    # Category → which agent roles are needed (beyond orchestrator + qa)
    TEAM_MAP: Dict[str, List[Dict[str, str]]] = {
        "website": [
            {"name": "platform-lead", "domain": "Platform", "model": "opus",
             "role": "lead", "routing": "(platform|arkitekt|design system|layout)"},
            {"name": "ui-builder", "domain": "UI", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(component|page|section|ui|html|css|style)"},
            {"name": "content-builder", "domain": "Content", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(content|text|copy|image|seo)"},
            {"name": "deploy-agent", "domain": "Deploy", "model": "haiku",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(deploy|host|build|ci|cd)"},
        ],
        "web-app": [
            {"name": "platform-lead", "domain": "Platform", "model": "opus",
             "role": "lead", "routing": "(platform|arkitekt|system design)"},
            {"name": "ui-builder", "domain": "UI/Frontend", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(component|page|ui|frontend|react|style)"},
            {"name": "api-builder", "domain": "API/Backend", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(api|endpoint|route|backend|database|server)"},
            {"name": "auth-builder", "domain": "Auth", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(auth|login|signup|session|permission)"},
            {"name": "deploy-agent", "domain": "Deploy", "model": "haiku",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(deploy|host|build|ci|cd)"},
        ],
        "saas": [
            {"name": "platform-lead", "domain": "Platform", "model": "opus",
             "role": "lead", "routing": "(platform|arkitekt|system design)"},
            {"name": "ui-builder", "domain": "UI/Frontend", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(component|page|ui|frontend|dashboard|react)"},
            {"name": "api-builder", "domain": "API/Backend", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(api|endpoint|route|backend|database|server)"},
            {"name": "auth-builder", "domain": "Auth", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(auth|login|signup|session|permission|billing)"},
            {"name": "infra-agent", "domain": "Infrastructure", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(infra|docker|ci|cd|deploy|monitor|scale)"},
        ],
        "e-commerce": [
            {"name": "platform-lead", "domain": "Platform", "model": "opus",
             "role": "lead", "routing": "(platform|arkitekt|system design)"},
            {"name": "ui-builder", "domain": "Storefront", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(component|page|product|cart|checkout|ui|style)"},
            {"name": "api-builder", "domain": "Backend", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(api|endpoint|inventory|order|payment|backend)"},
            {"name": "deploy-agent", "domain": "Deploy", "model": "haiku",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(deploy|host|build|ci|cd)"},
        ],
        "booking": [
            {"name": "platform-lead", "domain": "Platform", "model": "opus",
             "role": "lead", "routing": "(platform|arkitekt|system design)"},
            {"name": "ui-builder", "domain": "UI/Booking", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(component|page|calendar|booking|form|ui|style)"},
            {"name": "api-builder", "domain": "Backend", "model": "sonnet",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(api|endpoint|reservation|availability|backend)"},
            {"name": "deploy-agent", "domain": "Deploy", "model": "haiku",
             "role": "specialist", "parent": "platform-lead",
             "routing": "(deploy|host|build|ci|cd)"},
        ],
        "tool": [
            {"name": "code-lead", "domain": "Code", "model": "opus",
             "role": "lead", "routing": "(code|arkitekt|design|module)"},
            {"name": "builder", "domain": "Implementation", "model": "sonnet",
             "role": "specialist", "parent": "code-lead",
             "routing": "(build|implement|write|create|fix)"},
            {"name": "test-writer", "domain": "Testing", "model": "sonnet",
             "role": "specialist", "parent": "code-lead",
             "routing": "(test|spec|assert|coverage|verify)"},
        ],
        "api": [
            {"name": "code-lead", "domain": "API Architecture", "model": "opus",
             "role": "lead", "routing": "(api|arkitekt|schema|design|endpoint)"},
            {"name": "api-builder", "domain": "API Implementation", "model": "sonnet",
             "role": "specialist", "parent": "code-lead",
             "routing": "(build|implement|endpoint|route|handler)"},
            {"name": "test-writer", "domain": "Testing", "model": "sonnet",
             "role": "specialist", "parent": "code-lead",
             "routing": "(test|spec|assert|coverage|verify)"},
        ],
    }

    def _derive_team(self, blueprint: ProjectBlueprint) -> List[Dict[str, Any]]:
        """Derive agent team from project category + modules."""
        cat = blueprint.spec.category
        cat_key = cat.value if hasattr(cat, "value") else str(cat)

        # Base team: orchestrator + qa-lead (always present)
        team = [
            {"name": "orchestrator", "domain": "Coordination", "model": "opus",
             "role": "orchestrator", "routing": "(priorit|plan|architect|coordinat|delegat)"},
            {"name": "qa-lead", "domain": "Quality", "model": "sonnet",
             "role": "reviewer", "routing": "(review|granska|quality|qa|test|validat)"},
        ]

        # Category-specific agents
        category_agents = self.TEAM_MAP.get(cat_key, self.TEAM_MAP.get("web-app", []))
        team.extend(category_agents)

        # Module-driven additions
        spec = blueprint.spec
        if spec.has_auth and not any(a["name"] == "auth-builder" for a in team):
            lead = next((a["name"] for a in team if a["role"] == "lead"), "orchestrator")
            team.append({"name": "auth-builder", "domain": "Auth", "model": "sonnet",
                         "role": "specialist", "parent": lead,
                         "routing": "(auth|login|signup|session|permission)"})

        if spec.has_payment and not any("payment" in a.get("routing", "") for a in team):
            lead = next((a["name"] for a in team if a["role"] == "lead"), "orchestrator")
            team.append({"name": "payment-builder", "domain": "Payment", "model": "sonnet",
                         "role": "specialist", "parent": lead,
                         "routing": "(payment|checkout|stripe|billing)"})

        return team

    def _generate_agent_team(self, out: Path, blueprint: ProjectBlueprint) -> List[str]:
        """Generate agents/ directory with manifest + agent definition files."""
        agents_dir = out / "agents"
        agents_dir.mkdir(exist_ok=True)
        created = []

        team = self._derive_team(blueprint)
        project_name = self._spec_display_name(blueprint.spec)

        # Read vault agent templates
        vault_root = self._repo_root() / "vault" / "agents"

        # Generate agent manifest
        manifest = {
            "project": project_name,
            "generated": datetime.now().isoformat(),
            "category": blueprint.spec.category.value
            if hasattr(blueprint.spec.category, "value")
            else str(blueprint.spec.category),
            "agents": []
        }

        lead_names = [a["name"] for a in team if a["role"] == "lead"]
        specialist_names = [a["name"] for a in team if a["role"] == "specialist"]

        for agent in team:
            role = agent["role"]
            name = agent["name"]
            domain = agent["domain"]
            model = agent.get("model", "sonnet")
            routing = agent.get("routing", "")
            parent = agent.get("parent", "orchestrator")

            # Read the matching vault template
            template_path = vault_root / f"{role}.md"
            if template_path.is_file():
                content = template_path.read_text(encoding="utf-8")
            else:
                # Fallback: generate minimal agent definition
                content = self._minimal_agent_def(name, domain, model, role, routing, parent)

            # Fill placeholders
            content = content.replace("{{DOMAIN}}", domain)
            content = content.replace("{{DOMAIN_TITLE}}", f"{domain} Architecture")
            content = content.replace("{{SPECIALIST_NAME}}", name)
            content = content.replace("{{SPECIALIST_TITLE}}", domain)
            content = content.replace("{{PARENT_LEAD}}", parent)
            content = content.replace("{{ROUTING_PATTERNS}}", routing)
            content = content.replace("{{LEAD_AGENTS}}", ", ".join(lead_names))
            content = content.replace("{{SPECIALIST_AGENTS}}", ", ".join(
                [s["name"] for s in team if s.get("parent") == name]))
            content = content.replace("{{BUILDER_LEAD}}", lead_names[0] if lead_names else "orchestrator")
            content = content.replace("{{QA_LEAD}}", "qa-lead")
            content = content.replace("{{DEPLOY_AGENT}}",
                                      next((a["name"] for a in team if "deploy" in a["name"]), lead_names[0] if lead_names else "orchestrator"))

            # Overwrite the name in frontmatter
            if content.startswith("---"):
                lines = content.split("\n")
                for i, line in enumerate(lines[1:], 1):
                    if line.startswith("name:"):
                        lines[i] = f'name: "{name}"'
                        break
                    if line == "---":
                        break
                content = "\n".join(lines)

            created.append(self._write(agents_dir / f"{name}.md", content))

            # Add to manifest
            manifest["agents"].append({
                "name": name,
                "role": role,
                "domain": domain,
                "model": model,
                "routing_patterns": [routing] if routing else [],
                "reports_to": parent if role == "specialist" else
                              ("orchestrator" if role == "lead" else None),
            })

        # Write manifest
        created.append(self._write(
            agents_dir / "agent-manifest.json",
            json.dumps(manifest, indent=2, ensure_ascii=False)
        ))

        return created

    def _minimal_agent_def(self, name: str, domain: str, model: str,
                           role: str, routing: str, parent: str) -> str:
        """Fallback minimal agent definition when no vault template exists."""
        tools_by_role = {
            "orchestrator": "Read, Edit, Write, Bash, Glob, Grep, WebSearch, WebFetch, Agent",
            "lead": "Read, Edit, Write, Bash, Glob, Grep, Agent, WebSearch",
            "specialist": "Read, Edit, Write, Bash, Glob, Grep",
            "reviewer": "Read, Glob, Grep, Bash",
        }
        return f"""---
name: "{name}"
role: {role}
model: {model}
allowedTools: [{tools_by_role.get(role, tools_by_role["specialist"])}]
routing:
  patterns: ["{routing}"]
  fallback_to: "{parent}"
coordination:
  reports_to: "{parent}"
---

# {domain} — {role.title()}

## Identity
You are the {domain} {role} for this project.

## Responsibilities
- Execute {domain.lower()} tasks to production quality
- Follow project constraints (SYSTEM.md)
- Report completion to {parent}

## Constraints
- Follow SYSTEM.md code standards
- Report files created/modified

## Error Handling
Escalation: {name} → {parent} → orchestrator → human.
"""

    def _write(self, path: Path, content: str) -> str:
        path.write_text(content, encoding="utf-8")
        return str(path)

    def _spec_display_name(self, spec: ProjectSpec) -> str:
        if spec.project_name:
            return spec.project_name
        if spec.description:
            return spec.description[:50].strip() or "Project"
        return "Project"

    def _render_workspace_md(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        raw = self._read_template("WORKSPACE.md")
        if raw:
            return self._fill_placeholders(
                raw,
                {
                    "PROJECT_NAME": self._spec_display_name(spec),
                    "GENERATED_DATE": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "CATEGORY": spec.category.value
                    if hasattr(spec.category, "value")
                    else str(spec.category),
                    "STACK": spec.tech_stack.value
                    if hasattr(spec.tech_stack, "value")
                    else str(spec.tech_stack),
                    "MODULE_COUNT": str(len(bp.modules)),
                    "FEELING": spec.feeling or "Ej specificerat",
                    "LANGUAGES": ", ".join(spec.languages) or "en",
                },
            )
        return f"""# WORKSPACE: {self._spec_display_name(spec)}

> Generated by Buildr (Forge scaffold)
> {datetime.now().strftime("%Y-%m-%d %H:%M")}

See PROJECT.md, SYSTEM.md, MEMORY.md, TOOLS.md, RUN.md, state/orchestration.yaml, waves/, contracts/, modules/, qa/.
"""

    def _render_memory_stub(self, bp: ProjectBlueprint) -> str:
        return f"""# Project Memory (scaffold placeholder)

> When a full workspace is built via the bridge, this file is replaced with
> Imperfektum output. For a Forge-only scaffold, start recording notes here.

**Project:** {self._spec_display_name(bp.spec)}

## When We Knew It Was Done

_(Empty until you have a completed build to remember.)_
"""

    def _render_tools_stub(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        stack = (
            spec.tech_stack.value
            if hasattr(spec.tech_stack, "value")
            else str(spec.tech_stack)
        )
        integrations = ", ".join(spec.external_integrations) or "Inga ännu"
        return f"""# Tools (scaffold)

> Bridge-generated workspaces replace this with Index-selected tools. Until then,
> use PROJECT.md and your stack defaults.

**Stack:** {stack}
**Planned integrations:** {integrations}
"""

    def _render_run_md(self, bp: ProjectBlueprint) -> str:
        raw = self._read_template("RUN.md")
        if raw:
            return raw
        return """# Run

Agents: execute these steps in order.

1. Read **AGENT.md** for builder role, reading order, and gates.
2. Read **EVALUATOR.md** for evaluator review criteria and output expectations.
3. Read **MEMORY.md** for experience with this project.
4. Read **state/orchestration.yaml** for current progress.
5. If `onboarding_complete` is false → run `onboarding/prompt.md` (if present).
6. Find the first wave in **waves/** with status ≠ complete (see state file).
7. Load vault items declared in that wave.
8. Builder executes the wave steps.
9. Evaluator reviews the result and writes advisory feedback in `qa/evaluations/`.
10. Builder addresses evaluator feedback or records why no change is needed.
11. Run QA (`qa/checklist.md`). All checks must PASS.
12. Update **state/orchestration.yaml**.
13. Repeat from step 6 until all waves complete.
14. Report summary to user.
"""

    def _render_orchestration_yaml(self, bp: ProjectBlueprint,
                                    onboarding_complete: bool = False) -> str:
        spec = bp.spec
        proj = json.dumps(self._spec_display_name(spec))
        onboarding_flag = "true" if onboarding_complete else "false"

        # Register ALL waves (one per module)
        wave_entries = []
        for m in bp.modules:
            wave_id = f"{m.order:03d}-{m.id}"
            mod_file = f"{m.order:02d}-{m.id}.md"
            wave_entries.append(
                f'  "{wave_id}":\n'
                f'    status: pending\n'
                f'    module_order: {m.order}\n'
                f'    module_id: {json.dumps(m.id)}\n'
                f'    module_file: {json.dumps(mod_file)}'
            )
        waves_yaml = "\n".join(wave_entries)

        # Parallel phases
        parallel_yaml = ""
        if bp.build_phases:
            phase_lines = []
            for i, phase in enumerate(bp.build_phases, 1):
                ids_str = ", ".join(f'"{mid}"' for mid in phase)
                phase_lines.append(f"  phase_{i}: [{ids_str}]")
            parallel_yaml = "\nparallel_phases:\n" + "\n".join(phase_lines)

        first = min(bp.modules, key=lambda m: m.order)
        first_wave = f"{first.order:03d}-{first.id}"

        return f"""version: 2
contract_version: 1
onboarding_complete: {onboarding_flag}
phase: build
loc_budget: 10000
loc_consumed: 0
file_touch_budget: null
project_name: {proj}
category: {json.dumps(spec.category.value if hasattr(spec.category, "value") else str(spec.category))}
stack: {json.dumps(spec.tech_stack.value if hasattr(spec.tech_stack, "value") else str(spec.tech_stack))}
evaluation_mode: advisory
last_evaluation_summary: ""
current_wave: "{first_wave}"
next_wave: null
waves:
{waves_yaml}
{parallel_yaml}
decisions: []
derivations: []
vault_selections: {{}}
backlog: []
"""

    def _render_wave_for_module(self, module: ModuleSpec,
                                bp: ProjectBlueprint, wave_num: int) -> str:
        """Generate a prescriptive wave for a specific module."""
        spec = bp.spec
        mod_file = f"{module.order:02d}-{module.id}.md"
        wave_id = f"{wave_num:03d}-{module.id}"
        deps = ", ".join(module.depends_on) if module.depends_on else "Inga"

        # Determine tier from priority
        tier_map = {
            ModulePriority.FOUNDATION: "A",
            ModulePriority.CORE: "B",
            ModulePriority.FEATURE: "B",
            ModulePriority.ENHANCEMENT: "C",
            ModulePriority.DEPLOY: "C",
        }
        tier = tier_map.get(module.priority, "B")

        # Determine which parallel phase this module is in
        parallel_info = ""
        if bp.build_phases:
            for i, phase in enumerate(bp.build_phases, 1):
                if module.id in phase:
                    parallel_peers = [p for p in phase if p != module.id]
                    if parallel_peers:
                        parallel_info = (
                            f"\n## Parallel Group: Phase {i}\n\n"
                            f"This wave can run concurrently with: "
                            f"{', '.join(parallel_peers)}\n"
                        )
                    else:
                        parallel_info = (
                            f"\n## Parallel Group: Phase {i}\n\n"
                            f"This wave runs alone in its phase.\n"
                        )
                    break

        # Determine agent assignment from TEAM_MAP
        cat_key = spec.category.value if hasattr(spec.category, "value") else str(spec.category)
        agent_hint = self._suggest_agent_for_module(module, cat_key)

        # Generate imperative steps from module's files_to_create
        if module.files_to_create:
            file_steps = []
            for i, f in enumerate(module.files_to_create, 1):
                file_steps.append(f"{i}. Create `{f}` — implement per module spec")
            impl_steps = "\n".join(file_steps)
            extra_steps_offset = len(module.files_to_create)
        else:
            impl_steps = "1. Read the module spec and implement per description"
            extra_steps_offset = 1

        qa_step = extra_steps_offset + 1
        state_step = extra_steps_offset + 2

        # Acceptance criteria with IDs
        ac_prefix = module.id.upper().replace("-", "_")
        exit_criteria = "\n".join(
            f"- [ ] **AC-{ac_prefix}-{i:02d}:** {c}"
            for i, c in enumerate(module.acceptance_criteria, 1)
        )

        loc_estimate = max(200, len(module.files_to_create) * 80) if module.files_to_create else 500

        return f"""# Wave {wave_id}: {module.name}

## Intent
{module.description}

## Tier
{tier}

## Dependencies
{deps}
{parallel_info}
## Agent Assignment
Suggested: **{agent_hint}**

## Vault Items
Load these before executing (from vault-selection/):
- vault-selection/skills/ (relevant to: {module.id})
- vault-selection/constraints/ (tier {tier})
- vault-selection/routines/ (tier {tier})

## Module Spec
Read `modules/{mod_file}` for full specification including:
- Files to create ({len(module.files_to_create)} files)
- Data model ({len(module.data_model)} entities)
- Component specifications ({len(module.components)} components)
- User flow ({len(module.user_flows)} steps)

## Steps

{impl_steps}
{qa_step}. Run QA: verify all acceptance criteria below
{state_step}. Update state/orchestration.yaml: mark wave {wave_id} complete

## Exit Criteria

{exit_criteria}
- [ ] QA checklist passes for this wave
- [ ] state/orchestration.yaml updated (status: complete, loc_consumed)

## LOC Budget
Expected: {loc_estimate} lines

---

*Wave {wave_num} of {len(bp.modules)} | {bp.spec.project_name} | Stack: {spec.tech_stack.value if hasattr(spec.tech_stack, "value") else spec.tech_stack}*
"""

    def _suggest_agent_for_module(self, module: ModuleSpec, category: str) -> str:
        """Suggest which agent should handle this module based on its id."""
        ui_modules = {"design-system", "pages", "booking-catalog", "product-catalog",
                      "dashboard", "contact-form"}
        api_modules = {"auth", "data-management", "payment", "checkout",
                       "booking-calendar"}
        deploy_modules = {"deploy"}

        if module.id in deploy_modules:
            return "deploy-agent"
        if module.id == "foundation":
            return "platform-lead"
        if module.id in ui_modules:
            return "ui-builder"
        if module.id in api_modules:
            return "api-builder"
        return "platform-lead"

    def _render_contract_for_module(self, module: ModuleSpec,
                                     bp: ProjectBlueprint) -> str:
        """Generate a contract with actual interfaces for a module."""
        spec = bp.spec
        name = self._spec_display_name(spec)

        # Build interface section from data model and components
        interfaces = []

        if module.data_model:
            interfaces.append("### Data Entities\n")
            for entity_name, fields in module.data_model.items():
                field_lines = "\n".join(
                    f"  {fname}: {ftype}" for fname, ftype in fields.items()
                )
                interfaces.append(f"```\n{entity_name} {{\n{field_lines}\n}}\n```\n")

        if module.components:
            interfaces.append("### Components\n")
            for comp in module.components:
                interfaces.append(f"- `{comp}`")
            interfaces.append("")

        # Derive API endpoints from file list
        api_endpoints = []
        if module.files_to_create:
            for f in module.files_to_create:
                if "/api/" in f and f.endswith("route.ts"):
                    route_path = f.replace("src/app", "").replace("/route.ts", "")
                    route_path = route_path.replace("/[", "/:").replace("]", "")
                    if "[..." in f:
                        route_path = route_path.split("/[...")[0] + "/*"
                    api_endpoints.append(route_path)

        if api_endpoints:
            interfaces.append("### API Endpoints\n")
            for ep in api_endpoints:
                interfaces.append(f"- `GET/POST {ep}`")
            interfaces.append("")

        interfaces_text = "\n".join(interfaces) if interfaces else "- (Defined during implementation based on module spec.)\n"

        # Non-goals
        non_goals = ["- Features not listed in module spec", "- Performance optimization (deferred to deploy wave)"]
        if module.id != "auth":
            non_goals.append("- Authentication logic (handled by auth module)")

        return f"""# {module.name} — Contract

CONTRACT_VERSION: 1

## Decisions (locked — do not change without bumping version)

- Module: {module.id}
- Stack: {spec.tech_stack.value if hasattr(spec.tech_stack, "value") else spec.tech_stack}
- Priority: {module.priority.value}
- Dependencies: {', '.join(module.depends_on) or 'none'}

## Non-goals

{chr(10).join(non_goals)}

## Interfaces

{interfaces_text}

## Implementation Playbook

1. Read modules/{module.order:02d}-{module.id}.md for full specification.
2. Create files listed in module spec in dependency order.
3. Implement data model entities as defined above.
4. Build components with specified props/variants.
5. Follow user flow steps exactly.
6. Record cross-cutting decisions in this contract (bump CONTRACT_VERSION).

## Rules

- Do NOT add API endpoints not listed above or in module spec.
- Do NOT add data fields not defined in the data model.
- If unclear, STOP and ask — do not guess.
- Bump CONTRACT_VERSION if changing any interface above.
"""

    def _render_wave_foundation(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        first = min(bp.modules, key=lambda m: m.order)
        mod_file = f"{first.order:02d}-{first.id}.md"
        raw = self._read_template("waves/000-template.md")
        if raw:
            body = raw.replace("Wave NNN:", "Wave 001:").replace(
                "[Name]", first.name
            ).replace(
                "One sentence: what this wave produces.", f"Establish foundation for module {first.id}."
            ).replace(
                "A | B | C", "B"
            ).replace(
                "1. [Concrete action]\n2. [Concrete action]\n3. [Concrete action]",
                f"1. Read modules/{mod_file} and SYSTEM.md §Design.\n2. Implement per module spec; keep contracts in contracts/.\n3. Run QA for this wave; update state/orchestration.yaml."
            ).replace(
                "- [ ] [Measurable: builds without errors]\n- [ ] [Measurable: QA checklist passes]\n- [ ] [Measurable: state updated with loc_consumed]",
                "- [ ] Module acceptance criteria satisfied\n- [ ] QA checklist passes for this wave\n- [ ] state/orchestration.yaml updated (status, loc_consumed)"
            ).replace(
                "Expected: NNN lines",
                "Expected: 500 lines"
            )
        else:
            body = f"""# Wave 001: {first.name}

## Intent
Establish foundation before later modules (see modules/{mod_file}).

## Tier
B

## Vault Items
Load these before executing (adjust to wave intent):
- vault-selection/skills/file-structure.md
- vault-selection/constraints/dependency-discipline.md

## Steps
1. Read modules/{mod_file} and SYSTEM.md §Design.
2. Implement per module spec; keep contracts in contracts/.
3. Run QA for this wave; update state/orchestration.yaml.

## Exit Criteria
- [ ] Module acceptance criteria satisfied
- [ ] QA checklist passes for this wave
- [ ] state/orchestration.yaml updated (status, loc_consumed)

## LOC Budget
Expected: 500 lines
"""
        return f"""{body}

---

## Linked module

- `modules/{mod_file}` — primary spec for this foundation wave
- **Stack:** {spec.tech_stack.value if hasattr(spec.tech_stack, "value") else spec.tech_stack}
"""

    def _render_contract_foundation(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        raw = self._read_template("contracts/template.md")
        name = self._spec_display_name(spec)
        if raw:
            text = raw.replace("[Contract Name]", f"{name} — foundation").replace(
                "CONTRACT_VERSION: 1", "CONTRACT_VERSION: 1"
            )
        else:
            text = f"""# {name} — foundation
CONTRACT_VERSION: 1

## Decisions (locked — do not change without bumping version)
- Stack: {spec.tech_stack.value if hasattr(spec.tech_stack, "value") else spec.tech_stack}
- Category: {spec.category.value if hasattr(spec.category, "value") else spec.category}

## Non-goals
- Features not listed in PROJECT.md module specs

## Interfaces
- (Fill as APIs and schemas stabilize.)

## Implementation Playbook
1. Follow modules/ in order.
2. Record cross-cutting decisions here.
"""
        return text

    def _render_project(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        design = bp.design

        module_list = "\n".join(
            f"| {m.order} | {m.name} | {', '.join(m.depends_on) or '—'} | "
            f"{m.priority.value} |"
            for m in bp.modules
        )

        integration_list = ", ".join(spec.external_integrations) or "Inga"

        return f"""# {spec.project_name or 'Project'}

> Genererat av Project Forge v{spec.forge_version}
> Kategori: {spec.category.value}
> Skapat: {spec.created_at}

## Projektbeskrivning

{spec.description}

**Målgrupp:** {spec.target_audience}
**Plats/Kontext:** {spec.audience_location or 'Ej specificerat'}
**Språk:** {', '.join(spec.languages)}
**Känsla:** {spec.feeling or 'Ej specificerat'}

---

## Hard Constraints

```
HC-1: Läs WORKSPACE.md först, sedan övriga kärnfiler — bygg inte i blindo
HC-2: Bygg moduler I ORDNING — hoppa aldrig över beroenden
HC-3: Kör QA-checklistan (qa/checklist.md) EFTER varje modul
HC-4: Ändra ALDRIG designsystemet (SYSTEM.md §Design) mitt i bygget
HC-5: All output till disk — visa aldrig stora kodblock i konversation
HC-6: Fråga användaren vid osäkerhet — gissa aldrig
HC-7: Varje modul måste passera ALLA sina acceptanskriterier
HC-8: Följ RUN.md för orkestreringsloopen; använd RUNBOOK.md som modul-detalj — optimera aldrig ordningen
```

---

## Modulöversikt

| # | Modul | Beroenden | Prioritet |
|---|-------|-----------|-----------|
{module_list}

---

## Teknisk Stack

**Ramverk:** {spec.tech_stack.value}
**Databas:** {'Ja' if spec.needs_database else 'Nej'}
**API:** {'Ja' if spec.needs_api else 'Nej'}
**Integrationer:** {integration_list}
**Device-fokus:** {spec.audience_device}

---

## Designsystem (sammanfattning)

| Egenskap | Värde |
|----------|-------|
| Primärfärg | {design.primary} |
| Sekundärfärg | {design.secondary} |
| Accentfärg | {design.accent} |
| Bakgrund | {design.background} |
| Heading-font | {design.font_heading} |
| Body-font | {design.font_body} |
| Basstorlek | {design.base_size} |
| Border-radius | {design.border_radius} |
| Knappar | {design.button_style} |
| Kort | {design.card_style} |

Se SYSTEM.md §Design för fullständig specifikation.

---

## Deriveringslogg

Tekniska beslut härledda från användarens svar (aldrig frågade):

{chr(10).join(f'- {d}' for d in spec.derivation_log) or '- Inga deriveringar loggade'}
"""

    def _render_system(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        design = bp.design

        return f"""# Kvalitetsregler & Designsystem

> Denna fil styr hur projektet byggs — kodstandard, designregler, och kvalitetskrav.
> Ändra ALDRIG denna fil under bygget (HC-4).

---

## Kodstandard

- **Indentation:** 2 spaces (JS/TS/CSS), 4 spaces (Python)
- **Namnkonvention:** camelCase för variabler/funktioner, PascalCase för komponenter
- **Filnamn:** kebab-case (t.ex. `booking-calendar.tsx`)
- **Imports:** Grupperade: externa → interna → relativa, med blank rad mellan
- **Inga magic numbers** — alla värden som konstanter eller CSS-variabler
- **Inga hardcoded strings** — all synlig text i språkfiler eller konstanter
- **Inga inline styles** — allt i CSS/Tailwind

---

## Design

### Färger

```css
:root {{
  /* Primary */
  --color-primary: {design.primary};
  --color-primary-light: {design.primary_light};
  --color-primary-dark: {design.primary_dark};

  /* Secondary & Accent */
  --color-secondary: {design.secondary};
  --color-accent: {design.accent};

  /* Backgrounds */
  --color-bg: {design.background};
  --color-surface: {design.surface};

  /* Text */
  --color-text: {design.text_primary};
  --color-text-secondary: {design.text_secondary};

  /* Feedback */
  --color-error: {design.error};
  --color-success: {design.success};
}}
```

### Typografi

```css
:root {{
  --font-heading: '{design.font_heading}', system-ui, sans-serif;
  --font-body: '{design.font_body}', system-ui, sans-serif;
  --font-mono: '{design.font_mono}', monospace;
  --font-size-base: {design.base_size};
  --font-scale: {design.scale_ratio};
}}
```

### Spacing & Form

```css
:root {{
  --spacing: {design.spacing_unit};
  --radius: {design.border_radius};
  --max-width: {design.max_width};
}}
```

### Komponentstil

- **Knappar:** {design.button_style}
- **Kort:** {design.card_style}
- **Inputs:** {design.input_style}

---

## Responsivitet

Breakpoints (mobile-first):
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

{'**MOBILE-FIRST ÄR OBLIGATORISKT.** Design för mobil först, sedan skala upp.' if spec.audience_device == 'mobile-first' else 'Responsiv design krävs för alla breakpoints.'}

---

## Accessibility

- Kontrast: WCAG AA minimum (4.5:1 text, 3:1 stora element)
- Alt-text på alla bilder
- Tangentbordsnavigering fungerar
- Focus-indikatorer synliga
- Formulärfält med labels

---

## Förbjudna mönster

- Inline styles (`style=""`)
- `!important` i CSS (undantag: tredjepartsöverstyrning)
- Hardcoded färger (använd CSS-variabler)
- Bilder utan alt-text
- Knappar utan tillgängligt namn
- console.log i produktionskod
- Kommenterad-ut kod

---

## Språk & Tonalitet

**Primärspråk:** {spec.languages[0] if spec.languages else 'en'}
{f'**Ytterligare språk:** {", ".join(spec.languages[1:])}' if len(spec.languages) > 1 else ''}
**Känsla:** {spec.feeling or 'Professionell'}

---

*Deriverat från: {design.derived_from}*
"""

    def _render_runbook(self, bp: ProjectBlueprint) -> str:
        steps = []
        for m in bp.modules:
            deps = f" (kräver: {', '.join(m.depends_on)})" if m.depends_on else ""
            criteria = "\n".join(f"   - [ ] {c}" for c in m.acceptance_criteria)
            steps.append(f"""### Modul {m.order}: {m.name}{deps}

Läs `modules/{m.order:02d}-{m.id}.md` för fullständig spec.

{m.description}

**QA efter modulen:**
{criteria}

Alla checks måste passera innan du går vidare till nästa modul.

---
""")

        return f"""# RUNBOOK — Steg-för-steg

> **Canonical loop:** **RUN.md** (orchestration + waves + state).
> Denna fil är **kompletterande** modulförtydligande — inte motsägelse.
> Bygg i ordning. Hoppa aldrig. Efter varje modul: kör QA (qa/checklist.md).

---

## Innan du börjar

1. Läs **WORKSPACE.md** — överblick och filkontrakt
2. Läs **PROJECT.md** — hard constraints och modulöversikt
3. Läs **SYSTEM.md** — designsystem och kodstandard
4. Läs **RUN.md** — orkestreringsloop och state
5. Läs **denna fil** (RUNBOOK.md) — modulförtydligande
6. Bekräfta att du förstår innan du börjar bygga

---

{"".join(steps)}

## Efter alla moduler

1. Kör igenom hela qa/checklist.md — alla checks för alla moduler
2. Verifiera mot qa/acceptance.md — alla acceptanskriterier uppfyllda
3. Testa hela flödet end-to-end som en användare
4. Rapportera status till användaren

---

*Genererat av Project Forge v{bp.spec.forge_version}*
"""

    def _render_agent(self, bp: ProjectBlueprint) -> str:
        agent_template = self._read_template("AGENT.md")
        if agent_template:
            return agent_template
        return f"""# Builder Agent Instructions

> Denna fil styr hur du (agenten) arbetar med detta projekt.
> Läs denna fil vid sessionsstart och efter varje context compaction.

---

## Läsordning (före första modulen)

| # | Fil | Syfte |
|---|-----|-------|
| 0 | **WORKSPACE.md** | Överblick — läs först |
| 1 | **PROJECT.md** | Hard constraints, modulöversikt, teknisk stack |
| 2 | **SYSTEM.md** | Designsystem, kodstandard, kvalitetskrav |
| 3 | **MEMORY.md** | Erfarenhet, misstag, vad som fungerade |
| 4 | **TOOLS.md** | Tillgängliga verktyg / integrationer |
| 5 | **EVALUATOR.md** | Hur evaluatorn granskar och vad buildern ska göra med feedback |
| 6 | **RUN.md** | Kanonisk exekvering: state, waves, loop |
| 7 | **state/orchestration.yaml** | Status, fas, budget, vågprogress |
| 8 | **RUNBOOK.md** | Kompletterande modul-i-detalj (ej motsägelse mot RUN.md) |
| 9 | **modules/[aktuell].md** | Läs AKTUELL modul innan du bygger den |

---

## Execution Gate

Innan du bygger NÅGOT, bekräfta med egna ord:

```
EXECUTION CONFIRMATION
══════════════════════
Jag har läst WORKSPACE.md, PROJECT.md, SYSTEM.md, MEMORY.md, EVALUATOR.md och RUN.md. Jag bekräftar:

PROJEKTET:
  Kategori: {bp.spec.category.value}
  Stack: {bp.spec.tech_stack.value}
  Moduler: {len(bp.modules)} st, byggs i ordning

JAG KOMMER:
  ✓ Följa RUN.md och uppdatera state/orchestration.yaml
  ✓ Bygga moduler i ordning; använda RUNBOOK.md som detalj när det behövs
  ✓ Läsa varje modulfil innan jag bygger den
  ✓ Lämna över färdig wave/modul till evaluatorn innan jag går vidare
  ✓ Behandla evaluator-feedback som standardinput för nästa iteration
  ✓ Köra QA efter varje modul (alla checks PASS)
  ✓ Följa designsystemet i SYSTEM.md exakt
  ✓ Fråga vid osäkerhet — aldrig gissa

JAG KOMMER INTE:
  ✗ Hoppa över moduler eller ändra ordningen
  ✗ Ändra designsystemet mitt i bygget
  ✗ Skriva kod utan att ha läst modulspecen
  ✗ Ignorera evaluator-feedback utan att motivera varför
  ✗ Gå vidare om QA inte passerar
```

Invänta användarens godkännande innan du börjar.

---

## Per modul

1. Läs `waves/` + `state/orchestration.yaml` för aktuell våg (se RUN.md)
2. Läs `modules/[NN-module-name].md`
3. Bygg enligt specen; respektera `contracts/` där det finns beslut
4. Låt evaluatorn granska resultatet och skriva feedback i `qa/evaluations/`
5. Åtgärda evaluatorns viktigaste feedback eller notera varför ingen ändring krävs
6. Kör QA: `qa/checklist.md` → aktuell modul → alla checks PASS
7. Uppdatera state; rapportera kort: "Modul N klar. QA: X/X PASS."
8. Gå vidare till nästa modul

---

## Omstart (ny session / tappad kontext)

1. Läs denna fil (AGENT.md)
2. Läs MEMORY.md
3. Läs EVALUATOR.md
4. Läs state/orchestration.yaml
5. Återuppta första ofullständiga våg enligt RUN.md

---

## Felhantering

| Problem | Lösning |
|---------|---------|
| Osäker på implementation | Fråga användaren — gissa aldrig |
| Modul-QA failar | Fixa specifikt check som failar, kör QA igen |
| Designsystemet känns fel | Följ SYSTEM.md ändå — diskutera med användaren efteråt |
| Beroende saknas | Installera enligt PROJECT.md tech stack |
| Tredjepartstjänst otillgänglig | Implementera med mock/placeholder, notera för användaren |

---

*Genererat av Project Forge v{bp.spec.forge_version}*
"""

    def _render_evaluator(self, bp: ProjectBlueprint) -> str:
        category = bp.spec.category.value if hasattr(bp.spec.category, "value") else str(bp.spec.category)
        stack = bp.spec.tech_stack.value if hasattr(bp.spec.tech_stack, "value") else str(bp.spec.tech_stack)
        ui_categories = {"website", "booking", "e-commerce", "web-app", "saas"}
        if category in ui_categories:
            criteria = """1. **Design Quality** — is the output coherent and intentional?
2. **Originality** — does it avoid generic template or AI-slop patterns?
3. **Craft** — are spacing, hierarchy, and polish competent?
4. **Functionality** — does the implementation work for real user flows?"""
            review_mode = (
                "Use browser-based review by default when the relevant tools are available. "
                "Weight design quality and originality more heavily than craft and functionality."
            )
        else:
            criteria = """1. **Contract Fidelity** — does the output match the declared wave and module intent?
2. **Code Quality** — are naming, structure, and boundaries clear?
3. **Failure Handling** — are errors and edge cases handled properly?
4. **Operational Usability** — can a user or agent actually run and verify the result?"""
            review_mode = (
                "Browser-based review is optional here. Focus on contracts, code quality, "
                "failure handling, and operational usability."
            )

        return f"""# Evaluator Agent Instructions

> This file defines the evaluator role for this workspace.
> The evaluator is advisory by default and acts as the builder's critical counterweight.

## Identity

You are the evaluator agent.
You review completed work, search for quality gaps, and return structured feedback.
You do not exist to praise mediocre output.

## Project Context

- **Category:** {category}
- **Stack:** {stack}
- **Evaluation Mode:** advisory

## Criteria

{criteria}

## Default Review Mode

{review_mode}

## Output Contract

Write feedback to `qa/evaluations/latest.md`.
Each evaluation should include:
- scope reviewed
- summary judgment
- findings by severity
- recommended next actions
- whether browser-based review was used
"""

    def _render_evaluation_stub(self, bp: ProjectBlueprint) -> str:
        return """# Latest Evaluation

## Scope Reviewed

_No evaluation yet._

## Summary Judgment

_Pending._

## Findings

- None yet.

## Recommended Next Actions

- Complete the current wave and run evaluator review.

## Browser Validation

- Not run yet.
"""

    def _render_module(self, module: ModuleSpec, bp: ProjectBlueprint) -> str:
        deps = ", ".join(module.depends_on) if module.depends_on else "Inga"

        # Acceptance criteria with stable IDs
        ac_prefix = module.id.upper().replace("-", "_")
        criteria_lines = []
        for i, c in enumerate(module.acceptance_criteria, 1):
            ac_id = f"AC-{ac_prefix}-{i:02d}"
            criteria_lines.append(f"- [ ] **{ac_id}:** {c}")
        criteria = "\n".join(criteria_lines)

        custom = "\n".join(
            f"- **{k}:** {v}" for k, v in module.customization.items()
        ) if module.customization else "Inga projektspecifika anpassningar."

        # --- Prescriptive sections ---
        files_section = ""
        if module.files_to_create:
            file_list = "\n".join(f"- `{f}`" for f in module.files_to_create)
            files_section = f"""
---

## Filer att skapa

Skapa dessa filer i denna ordning (beroenden först):

{file_list}
"""

        data_section = ""
        if module.data_model:
            entities = []
            for entity_name, fields in module.data_model.items():
                field_lines = "\n".join(f"  - `{fname}`: {ftype}" for fname, ftype in fields.items())
                entities.append(f"### {entity_name}\n\n{field_lines}")
            data_section = f"""
---

## Datamodell

{chr(10).join(entities)}
"""

        components_section = ""
        if module.components:
            comp_list = "\n".join(f"- `{c}`" for c in module.components)
            components_section = f"""
---

## Komponenter

Skapa dessa komponenter med exakt dessa props/varianter:

{comp_list}
"""

        flow_section = ""
        if module.user_flows:
            flow_list = "\n".join(module.user_flows)
            flow_section = f"""
---

## Användarflöde (steg-för-steg)

Implementera exakt detta flöde:

{flow_list}
"""

        return f"""# Modul {module.order}: {module.name}

> Prioritet: {module.priority.value}
> Beroenden: {deps}

---

## Beskrivning

{module.description}

---

## Projektspecifik kontext

{custom}
{files_section}{data_section}{components_section}{flow_section}
---

## Acceptanskriterier

Alla måste vara uppfyllda innan modulen anses klar:

{criteria}

---

## Implementation

1. Läs SYSTEM.md §Design innan du implementerar visuella element.
2. Läs SYSTEM.md §Kodstandard innan du skriver kod.
3. Skapa filerna ovan i ordning.
4. Implementera komponenterna med angivna props.
5. Implementera användarflödet steg för steg.
6. Verifiera varje acceptanskriterium (markera med [x]).
7. Kör QA. Rapportera.

---

*Modul {module.order} av {len(bp.modules)} | {bp.spec.project_name}*
"""

    def _render_checklist(self, bp: ProjectBlueprint) -> str:
        sections = []
        for m in bp.modules:
            checks = "\n".join(f"- [ ] {c}" for c in m.acceptance_criteria)
            sections.append(f"""## Modul {m.order}: {m.name}

{checks}

---
""")

        return f"""# QA Checklista

> Kör efter varje modul. Alla checks måste passera (PASS) innan nästa modul.
> Markera med [x] när check passerar.

---

{"".join(sections)}

## Slutkontroll (efter alla moduler)

- [ ] Alla moduler passerar individuell QA
- [ ] End-to-end test: hela användarflödet fungerar
- [ ] Responsivitet: testat på 320px, 768px, 1024px
- [ ] Inga konsolfel i webbläsaren
- [ ] Inga brutna länkar
- [ ] Laddtid under 3 sekunder

---

*Genererat av Project Forge v{bp.spec.forge_version}*
"""

    def _render_acceptance(self, bp: ProjectBlueprint) -> str:
        spec = bp.spec
        return f"""# Acceptanskriterier

> Projektet är "klart" när ALLA dessa kriterier är uppfyllda.

---

## Funktionella krav

- Alla moduler byggda och QA-godkända (se qa/checklist.md)
- Alla användarflöden fungerar end-to-end
- Data persisterar korrekt (om databas används)
- Alla integrationer ({', '.join(spec.external_integrations) or 'inga'}) fungerar

## Designkrav

- Designsystemet (SYSTEM.md §Design) följs konsekvent
- Responsivt: fungerar på mobil, surfplatta, desktop
- Accessibility: WCAG AA-kontrast, tangentbordsnavigering
- Känslan matchar: "{spec.feeling or 'professionellt'}"

## Tekniska krav

- Inga konsolfel
- Inga brutna länkar
- Produktionsbygge fungerar
- Deployment-redo

## Projektspecifika krav

- Beskrivningen uppfylld: "{spec.description}"
- Målgruppen betjänad: "{spec.target_audience}"
{'- Betalning fungerar (test-mode)' if spec.has_payment else ''}
{'- Bokning fungerar end-to-end' if spec.has_booking else ''}
{'- Inloggning/registrering fungerar' if spec.has_auth else ''}

---

*Genererat av Project Forge v{bp.spec.forge_version}*
"""


# =============================================================================
# FORGE — MAIN ORCHESTRATOR
# =============================================================================

class ProjectForge:
    """
    Main orchestrator — maps to BACOWR's ArticleOrchestrator.

    Usage:
        forge = ProjectForge()

        # Onboarding
        questions = forge.get_questions(phase=1, level="standard")
        forge.process_answer("what", "...", "Booking site for fishing in Zanzibar", [...])
        forge.process_answer("who_for", "...", "Tourists visiting Zanzibar", [...])
        # ... more answers ...

        # Generate
        blueprint = forge.create_blueprint()
        files = forge.generate_scaffold(blueprint, output_dir="./my-project")
    """

    def __init__(self):
        self.onboarding = OnboardingEngine()
        self.design_deriver = DesignDeriver()
        self.module_resolver = ModuleResolver()
        self.scaffold_generator = ScaffoldGenerator()

    def get_questions(self, phase: int, level: str = "standard") -> List[Tuple[str, str, List[str]]]:
        """Get questions for a phase."""
        return self.onboarding.get_questions(phase, OnboardingLevel(level))

    def process_answer(self, question_id: str, question_text: str,
                       answer: str, signals: List[str]) -> List[str]:
        """Process one onboarding answer."""
        return self.onboarding.process_answer(question_id, question_text, answer, signals)

    def create_blueprint(self) -> ProjectBlueprint:
        """Create complete blueprint from onboarding data."""
        spec = self.onboarding.finalize()
        design = self.design_deriver.derive(spec)
        modules = self.module_resolver.resolve(spec)

        # Compute parallel build phases from module dependencies
        build_phases = self._compute_build_phases(modules)

        return ProjectBlueprint(
            spec=spec,
            design=design,
            modules=modules,
            build_phases=build_phases,
        )

    @staticmethod
    def _compute_build_phases(modules: List[ModuleSpec]) -> List[List[str]]:
        """Group modules into parallel execution phases based on dependencies.

        Modules in the same phase have all dependencies satisfied by prior phases.
        """
        completed: Set[str] = set()
        remaining = {m.id: set(m.depends_on) for m in modules}
        phases: List[List[str]] = []

        while remaining:
            # Find modules whose dependencies are all completed
            ready = [
                mid for mid, deps in remaining.items()
                if deps.issubset(completed)
            ]
            if not ready:
                # Circular dependency fallback: take one remaining module
                ready = [next(iter(remaining))]
            phases.append(sorted(ready))
            for mid in ready:
                completed.add(mid)
                del remaining[mid]

        return phases

    def generate_scaffold(self, blueprint: ProjectBlueprint,
                          output_dir: str) -> List[str]:
        """Generate the complete scaffold folder."""
        return self.scaffold_generator.generate(blueprint, output_dir)


# =============================================================================
# CLI
# =============================================================================

def main():
    """Interactive CLI for Project Forge."""
    import sys

    print("\n" + "=" * 60)
    print("  PROJECT FORGE v1.0")
    print("  From a conversation to a complete build system.")
    print("=" * 60)

    forge = ProjectForge()

    # Level selection
    print("\nVälj nivå:")
    print("  1. Express (5-7 frågor — snabbaste vägen)")
    print("  2. Standard (10-15 frågor — bra balans)")
    print("  3. Pro (15-25 frågor — mest kontroll)")
    level_choice = input("\nNivå [1/2/3]: ").strip()
    level_map = {"1": "express", "2": "standard", "3": "pro"}
    level = level_map.get(level_choice, "standard")

    # Run onboarding phases
    for phase in range(1, 4):
        questions = forge.get_questions(phase, level)
        for q_id, q_text, signals in questions:
            print(f"\n{q_text}")
            answer = input("> ").strip()
            if answer:
                derivations = forge.process_answer(q_id, q_text, answer, signals)
                if derivations:
                    print(f"  [Härledd: {', '.join(derivations)}]")

    # Create blueprint
    blueprint = forge.create_blueprint()

    # Show summary
    spec = blueprint.spec
    print(f"\n{'=' * 60}")
    print(f"  PROJEKTSAMMANFATTNING")
    print(f"{'=' * 60}")
    print(f"\n  Kategori: {spec.category.value}")
    print(f"  Stack: {spec.tech_stack.value}")
    print(f"  Moduler: {len(blueprint.modules)} st")
    print(f"  Integrationer: {', '.join(spec.external_integrations) or 'Inga'}")
    print(f"\n  Moduler som byggs:")
    for m in blueprint.modules:
        print(f"    {m.order}. {m.name} ({m.priority.value})")

    # Confirm
    print(f"\n  Stämmer det? [J/n]")
    confirm = input("> ").strip().lower()
    if confirm in ("n", "nej", "no"):
        print("Avbryter. Kör igen med justerade svar.")
        sys.exit(0)

    # Generate
    output_dir = input("\nOutput-mapp [./project-scaffold]: ").strip()
    output_dir = output_dir or "./project-scaffold"

    files = forge.generate_scaffold(blueprint, output_dir)

    print(f"\n{'=' * 60}")
    print(f"  SCAFFOLD GENERERAD")
    print(f"{'=' * 60}")
    print(f"\n  {len(files)} filer skapade i {output_dir}/")
    print(f"\n  Nästa steg:")
    print(f"  1. Öppna {output_dir}/ med din LLM (Claude Code, Codex, etc.)")
    print(f"  2. Be agenten läsa AGENT.md")
    print(f"  3. Projektet byggs autonomt")
    print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    main()
