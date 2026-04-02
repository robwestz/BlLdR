# Vault Index

Quick reference for all available building blocks.
Each item is self-contained and project-agnostic.

## Skills (35)

| File | Domain |
|------|--------|
| `accessibility-check` | WCAG AA compliance |
| `api-design` | REST endpoints |
| `auth-patterns` | Login, registration, sessions |
| `code-review` | Code quality review, systematic pass |
| `component-arch` | UI component architecture, composition |
| `component-creation` | React/UI components |
| `dark-mode` | Theme switching, CSS variables, persistence |
| `data-fetch` | Remote data, loading/error/empty states, caching |
| `data-modeling` | Types, schemas, entities |
| `database-schema` | Schema naming, normalization, migrations, indexes |
| `deploy-checklist` | Production readiness |
| `drag-drop` | Drag-and-drop lists, reorder, drop zones |
| `environment-config` | Env vars, secrets, per-environment config |
| `error-boundary` | React error boundaries, fallback UI, recovery |
| `error-handling` | Try/catch, loading, empty states |
| `file-structure` | Project organization |
| `file-upload` | Upload flow, type validation, storage |
| `form-validation` | User input, forms |
| `i18n` | Multi-language support |
| `implementation-playbook` | Module spec → working code step by step |
| `contract-authoring` | Interface contracts between modules |
| `logging-observability` | Structured logging, correlation IDs, health checks |
| `input-sanitization` | Sanitize user input before storage or display |
| `modal-dialog` | Focus trap, keyboard nav, scroll lock |
| `notification-system` | Toast/snackbar: timing, types, accessibility |
| `pagination` | Offset/cursor pagination, infinite scroll |
| `payment-flow` | Checkout, payment integration |
| `performance` | Load time, bundle size |
| `realtime-updates` | WebSocket, SSE, polling — choosing and wiring |
| `research` | Systematic topic research before decisions |
| `responsive-layout` | CSS, viewport adaptation |
| `search-filter` | Client/server search, debounce, URL-persisted state |
| `seo` | Search engine optimization |
| `state-design` | Where state lives |
| `testing-strategy` | What and how to test |

## Constraints (16)

| File | Prohibits |
|------|-----------|
| `accessibility` | Missing alt text, labels, contrast |
| `code-hygiene` | Commented-out code, unused imports/vars |
| `dependency-discipline` | Unjustified npm packages |
| `no-console-log` | console.log in production code |
| `no-empty-catch` | Empty or silent catch/except blocks |
| `no-direct-db-in-ui` | Database calls from client-side components |
| `no-hardcoded-values` | Magic numbers, inline colors, hardcoded strings |
| `no-implicit-any` | TypeScript `any` without annotation + comment |
| `no-inline-styles` | Style attributes in JSX/HTML |
| `no-magic-routes` | Hard-coded URL strings; require route constants |
| `no-placeholder-content` | Lorem ipsum, example@, placeholder images |
| `no-sync-in-async` | Blocking sync operations inside async functions |
| `no-untyped-props` | React components without TypeScript prop interfaces |
| `performance` | Unoptimized images, blocking resources |
| `security` | XSS, exposed secrets, injection |
| `token-budget` | Excessive comments, speculative code |

## Strategies (14)

| File | Thinking Pattern |
|------|-----------------|
| `build-order` | What to build first |
| `contract-first` | Interface before implementation |
| `decomposition` | Breaking large tasks into steps |
| `error-first` | Failure modes before happy path |
| `error-vs-feature` | When to fix a bug vs continue building |
| `mobile-first` | Small screen → large screen |
| `progressive-enhancement` | Simple → complex in layers |
| `scope-cut` | How to reduce scope without cutting quality |
| `tech-choice` | How to pick between technology options |
| `test-scope` | What deserves a test; when to skip |
| `when-to-abstract` | Concrete vs generic |
| `parallel-wave-execution` | Run independent waves concurrently |
| `preflight-reopen` | When approved preflight may be changed |
| `when-to-cache` | When caching adds value vs complexity |

## Routines (15)

| File | Trigger |
|------|---------|
| `accessibility-audit` | After any UI module |
| `api-endpoint-check` | After implementing any API endpoint |
| `code-complete` | Before marking code unit as done |
| `database-migration-check` | Before running any database migration |
| `dependency-audit` | When adding or updating packages |
| `performance-check` | After any deployment |
| `post-module-qa` | After every module (all types) |
| `pre-commit` | Before any git commit |
| `pre-deploy` | Before any production deployment |
| `responsive-verify` | After any visual change |
| `retrospective` | After every phase/wave |
| `security-check` | Before exposing any endpoint to the internet |
| `preflight-gate-check` | Before starting workspace generation (advanced flow) |
| `wave-parallel-merge` | After parallel waves complete, before next phase |
| `wave-handoff` | Before ending session mid-wave, or at wave completion |

## Memories (20)

| File | Scope |
|------|-------|
| `universal-scars` | All projects |
| `universal-insights` | All projects |
| `execution/builder-evaluator-memories` | Builder/evaluator execution loops |
| `execution/wave-handoff-memories` | Session and wave handoffs |
| `execution/qa-regression-memories` | QA depth and regression prevention |
| `execution/rework-drift-memories` | Scope drift, rework loops, execution control |
| `category/api-memories` | REST API / backend service projects |
| `category/booking` | Booking/reservation projects |
| `category/dashboard-memories` | Admin/analytics dashboard projects |
| `category/ecommerce` | E-commerce/shop projects |
| `category/saas` | SaaS/subscription projects |
| `category/tool` | CLI tools, scripts |
| `category/webapp` | Web app with auth/dashboard |
| `category/website` | Marketing/content sites |
| `stack/nextjs` | Next.js projects |
| `stack/prisma-memories` | Prisma ORM usage |
| `stack/python` | Python projects |
| `stack/react-vite` | React + Vite projects |
| `stack/static-html` | Static HTML sites |
| `stack/typescript-memories` | TypeScript-specific patterns |

## Agent Templates (4)

| File | Role | Model |
|------|------|-------|
| `agents/orchestrator` | Apex coordinator — delegates, never codes | opus |
| `agents/lead` | Domain lead — owns architecture, delegates to specialists | opus |
| `agents/specialist` | Focused implementer — executes specs from lead | sonnet |
| `agents/reviewer` | QA gatekeeper — skeptical review, pass/fail verdicts | sonnet |
