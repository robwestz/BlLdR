# BUILDR RESCUE — System Architecture
## The Halfway House Pattern

> Import broken projects. Diagnose them. Fix them. Ship them.

---

## Why This Exists

Every developer has abandoned projects. Every team has codebases that
"someone started but nobody finished." Every freelancer inherits code
from the previous developer. These projects share a pattern:

1. They built SOMETHING — there's real code, real decisions, real progress
2. Something went wrong — a bug, a bad architecture choice, scope creep, burnout
3. Now it sits there — too much work invested to delete, too broken to use

The Rescue skill turns these dead projects into living ones.

---

## How Rescue Differs from Operator

| Aspect | Operator | Rescue |
|--------|----------|--------|
| Starting point | Zero — blank canvas | Existing code — someone else's decisions |
| Workspace location | New directory | `.buildr/` overlay inside existing project |
| First wave | Foundation (scaffold, design system) | Make it buildable (fix deps, config) |
| Design system | Derived from user description | Extracted from existing CSS/config |
| Architecture | Chosen by Forge | Accepted as-is (unless it's the root cause) |
| Imperfektum | Fabricated memories | Real memories from diagnosis |
| Agent attitude | Creative builder | Conservative surgeon |
| Goal | Build something new | Make something broken work |

---

## The Diagnosis Engine

### What Makes a Good Diagnosis

A good diagnosis is:
- **Specific** — "line 47 of api/routes.ts catches errors with empty blocks"
  not "error handling could be improved"
- **Evidenced** — "npm run build outputs: Module not found '@types/node'"
  not "might be missing types"
- **Causal** — "missing @types/node causes TypeScript compilation to fail
  which blocks the build" not just "build is broken"
- **Actionable** — "add @types/node to devDependencies" not "fix the build"

### Diagnosis Categories

```
BUILD_FAILURE     — Can't compile, can't start, can't install deps
RUNTIME_ERROR     — Crashes during normal usage
MISSING_FEATURE   — Described in docs/UI but not implemented
BROKEN_FEATURE    — Implemented but doesn't work correctly
DEAD_CODE         — Files/functions that are never called
CONFIG_ISSUE      — Wrong env vars, missing config, bad paths
SECURITY_ISSUE    — Exposed secrets, missing auth, SQL injection
ARCHITECTURE_DEBT — Patterns that cause cascading problems
TYPE_SAFETY       — Missing types, any/unknown overuse
TEST_GAP          — Critical paths without tests
```

### Severity Definitions

**BLOCKER** — The project cannot run, build, or deploy.
Examples: missing dependencies, syntax errors, missing env vars,
database connection failures.

**MAJOR** — Core features don't work correctly.
Examples: broken forms, 500 errors on main routes, auth bypass,
data corruption, missing error handling.

**MINOR** — Quality/polish issues that don't break functionality.
Examples: console.log left in, missing loading states, no mobile
responsiveness, accessibility gaps, missing types.

---

## The .buildr/ Overlay Pattern

The key architectural decision: Rescue does NOT restructure the existing
project. It creates a `.buildr/` directory that acts as a control layer.

```
my-broken-project/
├── src/                    ← Existing code (UNTOUCHED during wrap)
├── package.json            ← Existing config (UNTOUCHED during wrap)
├── .env                    ← Existing env (UNTOUCHED during wrap)
│
└── .buildr/                ← Rescue overlay
    ├── WORKSPACE.md        ← "This is a rescue project. Here's what's wrong."
    ├── diagnosis/          ← Full diagnostic evidence
    ├── waves/              ← Fix plan (references files in parent directory)
    ├── agents/             ← Team for fixing this project
    └── state/              ← Progress tracking
```

Wave files reference paths relative to the project root (parent of .buildr/):
```markdown
## Steps
1. Fix `../src/api/routes.ts:47` — add error handling to catch block
2. Fix `../package.json` — add @types/node to devDependencies
```

### Why Overlay, Not Merge?

1. **Reversible** — `rm -rf .buildr/` removes all Rescue traces
2. **Non-conflicting** — no existing file is modified until wave execution
3. **Git-friendly** — `.buildr/` is one directory, easy to .gitignore or commit
4. **Familiar** — same pattern as `.github/`, `.vscode/`, `.husky/`

---

## Integration with Project Registry

Rescue projects are registered with `origin: "rescue"` which:

1. Shows `[R]` flag in project listings
2. Tells agents: "this is existing code, not greenfield"
3. Enables rescue-specific memory queries
4. Tracks original diagnosis alongside wave progress

```bash
# Register a rescue
project-registry.sh --register --name "client-app" \
  --path "/home/robin/projects/client-app" \
  --category "web-app" --origin "rescue"

# List shows origin
project-registry.sh --list
# > [R] client-app           in_progress     wave 001  (2026-03-27)
```

---

## Agent Team for Rescue Projects

Rescue projects get a specialized team:

| Agent | Role in Rescue |
|-------|---------------|
| orchestrator | Coordinates fix waves, prioritizes issues |
| platform-lead | Makes architecture decisions about which patterns to preserve |
| bug-fixer (specialist) | Implements specific fixes from diagnosis |
| qa-lead | Verifies fixes don't introduce regressions |

The team is smaller than greenfield because:
- There's no design system to build (it exists)
- There's no scaffolding to create (it exists)
- The focus is surgical fixes, not creative building

---

## Example: Rescuing a Next.js App

### Intake
```
PROJECT: nomo-dashboard
STACK: Next.js 15 + TypeScript + Prisma + Tailwind
FILES: 127 files, 8,400 lines
LAST_COMMIT: 2026-03-10 by robin — "wip: dashboard layout"
HAS_TESTS: no
HAS_CI: no
```

### Diagnosis
```
BLOCKER: npm install fails — prisma@5.x conflicts with @prisma/client@4.x
BLOCKER: .env.local missing DATABASE_URL — app crashes on start
MAJOR: /api/users endpoint returns 500 — Prisma schema mismatch
MAJOR: Dashboard page shows blank — useEffect fetches wrong endpoint
MINOR: No error boundaries — any component crash = white screen
MINOR: No loading states — fetch shows nothing until complete
MINOR: Tailwind purge not configured — CSS is 2MB in production
```

### Fix Plan
```
Wave 1: Make it run (2 BLOCKERS)
  - Fix prisma version conflict
  - Create .env.example with all required vars

Wave 2: Fix core features (2 MAJOR)
  - Fix Prisma schema → run migration
  - Fix dashboard fetch endpoint

Wave 3: Resilience (3 MINOR)
  - Add error boundaries
  - Add loading states
  - Configure Tailwind purge

Wave 4: Verify
  - Full smoke test of all routes
  - All diagnosis issues confirmed fixed
```
