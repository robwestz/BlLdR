"""
vault_selector.py — Picks relevant Vault items for a given wave/module.

Stateless. Takes a wave intent + tier → returns file paths to load.
"""
from pathlib import Path
from typing import List, Dict

VAULT_ROOT = Path(__file__).parent.parent / "vault"

# Maps keywords in wave intent to vault skill filenames.
# One keyword can map to multiple skills (list) or a single skill (string).
SKILL_KEYWORDS: dict = {
    # --- Forms & input ---
    "form": "form-validation.md",
    "input": "form-validation.md",
    "validation": "form-validation.md",
    "sanitize": "input-sanitization.md",
    "sanitization": "input-sanitization.md",
    "xss": "input-sanitization.md",
    "injection": "input-sanitization.md",
    # --- Layout & responsive ---
    "responsive": "responsive-layout.md",
    "layout": "responsive-layout.md",
    "mobile": "responsive-layout.md",
    "dark mode": "dark-mode.md",
    "dark theme": "dark-mode.md",
    "theme": "dark-mode.md",
    # --- Components ---
    "component": "component-creation.md",
    "button": "component-creation.md",
    "card": "component-creation.md",
    "component architecture": "component-arch.md",
    "component arch": "component-arch.md",
    "composition": "component-arch.md",
    "modal": "modal-dialog.md",
    "dialog": "modal-dialog.md",
    "overlay": "modal-dialog.md",
    "notification": "notification-system.md",
    "toast": "notification-system.md",
    "snackbar": "notification-system.md",
    "drag": "drag-drop.md",
    "sortable": "drag-drop.md",
    "reorder": "drag-drop.md",
    # --- Data & state ---
    "data model": "data-modeling.md",
    "entity": "data-modeling.md",
    "schema": ["data-modeling.md", "database-schema.md"],
    "database": "database-schema.md",
    "migration": "database-schema.md",
    "sql": "database-schema.md",
    "table": "database-schema.md",
    "fetch": "data-fetch.md",
    "remote data": "data-fetch.md",
    "api call": "data-fetch.md",
    "pagination": "pagination.md",
    "paginate": "pagination.md",
    "infinite scroll": "pagination.md",
    "search": "search-filter.md",
    "filter": "search-filter.md",
    "state": "state-design.md",
    "context": "state-design.md",
    "hook": "state-design.md",
    # --- Errors & resilience ---
    "error": "error-handling.md",
    "loading": "error-handling.md",
    "empty state": "error-handling.md",
    "error boundary": "error-boundary.md",
    "crash": "error-boundary.md",
    "fallback": "error-boundary.md",
    # --- API & backend ---
    "api": "api-design.md",
    "endpoint": "api-design.md",
    "rest": "api-design.md",
    "upload": "file-upload.md",
    "file upload": "file-upload.md",
    "attachment": "file-upload.md",
    "realtime": "realtime-updates.md",
    "websocket": "realtime-updates.md",
    "sse": "realtime-updates.md",
    "polling": "realtime-updates.md",
    "live update": "realtime-updates.md",
    # --- Config & infra ---
    "env": "environment-config.md",
    "environment": "environment-config.md",
    "secret": "environment-config.md",
    "config": "environment-config.md",
    "deploy": "deploy-checklist.md",
    "production": "deploy-checklist.md",
    # --- Quality ---
    "accessibility": "accessibility-check.md",
    "wcag": "accessibility-check.md",
    "a11y": "accessibility-check.md",
    "file structure": "file-structure.md",
    "project setup": "file-structure.md",
    "testing": "testing-strategy.md",
    "test": "testing-strategy.md",
    "review": "code-review.md",
    "code review": "code-review.md",
    # --- I18n & SEO ---
    "i18n": "i18n.md",
    "language": "i18n.md",
    "translation": "i18n.md",
    "seo": "seo.md",
    "meta tag": "seo.md",
    # --- Auth & payments ---
    "auth": "auth-patterns.md",
    "login": "auth-patterns.md",
    "payment": "payment-flow.md",
    "checkout": "payment-flow.md",
    "stripe": "payment-flow.md",
    # --- Performance ---
    "performance": "performance.md",
    "optimize": "performance.md",
    "speed": "performance.md",
}

TIER_CONSTRAINTS = {
    # Foundation: architecture + type safety + security boundaries
    "A": [
        "code-hygiene.md", "dependency-discipline.md", "token-budget.md",
        "no-hardcoded-values.md", "security.md",
        "no-untyped-props.md", "no-direct-db-in-ui.md",
    ],
    # Feature: presentation layer + runtime safety
    "B": [
        "code-hygiene.md", "no-hardcoded-values.md", "no-inline-styles.md",
        "no-placeholder-content.md", "no-console-log.md",
        "no-magic-routes.md", "no-implicit-any.md",
    ],
    # Polish/integration: output quality + async safety
    "C": [
        "code-hygiene.md", "no-inline-styles.md", "no-console-log.md",
        "no-placeholder-content.md", "accessibility.md",
        "performance.md", "no-sync-in-async.md",
    ],
}

TIER_ROUTINES = {
    # Foundation: verify structure, track dependencies, debrief
    "A": ["post-module-qa.md", "retrospective.md", "dependency-audit.md", "pre-commit.md"],
    # Feature: verify UI quality + security exposure
    "B": ["post-module-qa.md", "responsive-verify.md", "pre-commit.md", "security-check.md"],
    # Polish/integration: completeness + production readiness
    "C": ["code-complete.md", "responsive-verify.md", "performance-check.md"],
}


def select_skills(intent: str) -> List[str]:
    """Select vault skills matching the wave's intent."""
    intent_lower = intent.lower()
    selected = set()
    for keyword, filename in SKILL_KEYWORDS.items():
        if keyword in intent_lower:
            path = VAULT_ROOT / "skills" / filename
            if path.exists():
                selected.add(str(path))
    return sorted(selected)


def select_constraints(tier: str) -> List[str]:
    """Select vault constraints for the given tier."""
    tier = tier.upper()
    filenames = TIER_CONSTRAINTS.get(tier, TIER_CONSTRAINTS["C"])
    return [str(VAULT_ROOT / "constraints" / f)
            for f in filenames if (VAULT_ROOT / "constraints" / f).exists()]


def select_routines(tier: str) -> List[str]:
    """Select vault routines for the given tier."""
    tier = tier.upper()
    filenames = TIER_ROUTINES.get(tier, TIER_ROUTINES["C"])
    return [str(VAULT_ROOT / "routines" / f)
            for f in filenames if (VAULT_ROOT / "routines" / f).exists()]


def select_memories(category: str = "", stack: str = "") -> List[str]:
    """Select relevant Imperfektum memory templates."""
    memories = [
        str(VAULT_ROOT / "memories" / "universal-scars.md"),
        str(VAULT_ROOT / "memories" / "universal-insights.md"),
    ]
    if category:
        cat_path = VAULT_ROOT / "memories" / "category" / f"{category}.md"
        if cat_path.exists():
            memories.append(str(cat_path))
    if stack:
        stack_path = VAULT_ROOT / "memories" / "stack" / f"{stack}.md"
        if stack_path.exists():
            memories.append(str(stack_path))
    return memories


def select_for_wave(intent: str, tier: str,
                    category: str = "", stack: str = "") -> Dict[str, List[str]]:
    """One-call selection: returns all vault items for a wave."""
    return {
        "skills": select_skills(intent),
        "constraints": select_constraints(tier),
        "routines": select_routines(tier),
        "memories": select_memories(category, stack),
    }
