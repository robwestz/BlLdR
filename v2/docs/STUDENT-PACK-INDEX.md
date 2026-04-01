# GitHub Student Developer Pack -- Buildr Service Index

This file indexes every service in the GitHub Student Developer Pack, categorized by relevance to the Buildr system (an agent-orchestrated, layered build system that takes a prompt and produces deployable software via preflight, workspace generation, and wave-based execution). Agents should scan the tier that matches their current task. Tier 4 contains non-obvious but specific integrations worth reading even if they seem unrelated at first glance.

---

## Tier 1: Direct Infrastructure

Services that host, deploy, run, or directly enable buildr-nu and its generated workspaces.

| Service | Free Offer | Buildr Use | Concrete One-Time Action |
|---------|-----------|------------|--------------------------|
| **DigitalOcean** | $200 platform credit for 1 year | Primary hosting for buildr-nu (landing, API, docs), staging environments for generated workspaces | Provision a $6/mo droplet running the buildr-nu site + a separate staging droplet where executor-generated workspaces are auto-deployed via GitHub Actions for live QA |
| **Heroku** | $13/mo credit for 24 months ($312 total) | Secondary deploy target and preview-app host for generated workspaces | Create a Heroku pipeline with staging + production apps; configure auto-deploy from the buildrhel repo's main branch so every merged workspace gets a live review URL |
| **Microsoft Azure** | $100 credit + 25 free services | Cloud functions for Forge/Bridge engines, blob storage for preflight artifacts, Azure DevOps for CI | Deploy the Forge engine as an Azure Function triggered by webhook; store approved PREFLIGHT_APPROVAL.json artifacts in Azure Blob with immutable retention policy |
| **GitHub Pro** | Free while student | Private repos, advanced code review, required reviewers, Pages, Actions minutes | Enable branch protection on `main` requiring preflight-approval status check; configure GitHub Actions to run the 51-test suite on every PR |
| **GitHub Codespaces** | Free Pro access | Instant dev environment for contributors; pre-configured with Python deps, engines, vault | Create a `.devcontainer/devcontainer.json` that installs all Buildr dependencies so any contributor opens the repo in a working Codespace in under 90 seconds |
| **GitHub Pages** | Unlimited project sites | Host buildr-nu public docs, vault item browser, generated workspace documentation | Deploy a static site from `docs/` to `buildr-nu.github.io` that renders the vault INDEX, skill catalog, and system architecture as browsable HTML |
| **Appwrite** | Free Education plan (equiv. Pro, $15/mo) | Backend-as-a-Service for buildr-nu: auth, database, storage, serverless functions | Set up an Appwrite project with: users collection (waitlist), projects collection (generated workspaces metadata), storage bucket (preflight artifacts), and auth flow for the buildr-nu dashboard |
| **GitHub Copilot** | Free Copilot Pro | AI pair programming during executor wave execution; autocomplete for generated workspace code | Enable Copilot in the repo settings; agents working in generated workspaces get AI-assisted code completion that accelerates wave execution |
| **LocalStack** | Free Pro license | Emulate AWS services locally for workspaces that target AWS deployment (Lambda, S3, DynamoDB) | Configure a `docker-compose.localstack.yml` in the templates directory so any generated workspace with AWS dependencies can run `docker compose up` and test against local AWS emulation |
| **Namecheap** | 1 year .me domain + 1 SSL cert | Domain for buildr-nu or a showcase workspace | Register `buildr.me` (or similar), configure SSL, point DNS to DigitalOcean droplet -- gives the project a permanent, professional URL |
| **Name.com** | Free domain (.live/.studio/.software/.app/.dev) | Additional domain for buildr-nu or specific showcase | Register `buildr.software` or `buildr.dev` as the canonical project domain with HTTPS |
| **.TECH** | 1 free .tech domain for 1 year | Branded domain for technical documentation or API endpoint | Register `buildr.tech` and point it to the GitHub Pages documentation site |
| **Stripe** | Waived fees on first $1000 revenue | Payment processing for buildr-nu paid tier (workspace generation as a service) | Integrate Stripe Checkout into buildr-nu; create a product for "Workspace Generation" with a $X/workspace price; wire the webhook to mark workspaces as paid |
| **MongoDB** | $50 Atlas credits + free certification | Document store for session state, discovery logs, preflight artifact metadata, wave execution history | Create a MongoDB Atlas cluster; define collections for `sessions`, `discoveries`, `preflight_runs`, `workspaces`; migrate the JSONL continuum data into queryable documents |

---

## Tier 2: Quality & Observability

Services that monitor, test, secure, or ensure quality of Buildr and its generated outputs.

| Service | Free Offer | Buildr Use | Concrete One-Time Action |
|---------|-----------|------------|--------------------------|
| **Sentry** | 50K errors, 100K transactions, 1GB attachments, 500 replays for 1 year | Error tracking across Forge/Bridge engines, executor runtime, and generated workspace apps | Install `sentry-sdk` in `engines/`; configure DSN in environment; add Sentry init to the generated workspace CLAUDE.md template so every built app ships with error tracking from wave 1 |
| **Datadog** | Pro account, 10 servers, free 2 years | Infrastructure monitoring for DigitalOcean/Heroku hosts, APM for engine execution times, log aggregation | Install the Datadog agent on the DigitalOcean droplet; create dashboards for: engine execution latency, preflight pass/fail rates, workspace generation success rate, deploy health |
| **New Relic** | Free student plan ($300/mo value) | Full-stack observability: APM for Python engines, browser monitoring for buildr-nu frontend, synthetic checks | Set up New Relic APM for the Forge engine; create a synthetic monitor that runs the preflight-to-workspace flow every hour and alerts on failure |
| **Honeybadger** | Free Small account for 1 year | Exception and uptime monitoring with cron monitoring for scheduled tasks | Configure Honeybadger check-ins for the memory-system cron jobs (discovery mining, context distillation); get alerted if any scheduled maintenance task silently fails |
| **Codecov** | Free on public and private repos | Code coverage tracking for the 51-test suite; enforce coverage thresholds on PRs | Add Codecov GitHub Action to CI; upload coverage from `pytest --cov`; set a 80% minimum coverage gate on PRs touching `engines/` |
| **Travis CI** | Free private builds | Secondary CI for cross-platform testing (the repo targets Windows but engines are Python) | Configure `.travis.yml` to run the test suite on Ubuntu and macOS, catching platform-specific bugs in bash scripts under `memory-system/tools/` |
| **BrowserStack** | Free Automate Mobile Plan for 1 year | Cross-browser testing for buildr-nu frontend and generated workspace web apps | Write a Selenium test that opens a generated workspace's deployed URL on Chrome, Firefox, Safari, and mobile Safari via BrowserStack; run it in CI after deploy |
| **LambdaTest** | Free Live Plan for 1 year | Live interactive cross-browser testing for UI-heavy generated workspaces | Create a LambdaTest tunnel to the local dev server; test generated booking/e-commerce workspaces across 10 browser/OS combos before marking wave as PASS |
| **Blackfire** | Free Developer subscription | Performance profiling for Python engines (Forge, Imperfektum, Vault Selector) | Profile `forge_engine.py` workspace generation with Blackfire; identify and fix the slowest module resolution paths; document baseline performance in a discovery |
| **CodeScene** | Free Student account for private repos | Behavioral code analysis: identify hotspots, coupling, and tech debt in the Buildr repo itself | Connect CodeScene to the buildrhel repo; run initial analysis; use the hotspot map to prioritize which engine files need refactoring in `v2/improve.md` |
| **DeepScan** | Free 6-month trial | Static analysis for JavaScript/TypeScript in generated workspaces (NextJS stack) | Enable DeepScan on the repo; add a CI check that scans generated workspace JS/TS code for bugs before the evaluator runs |
| **AstraSecurity** | 6 months firewall + malware scanner | Web application firewall for the deployed buildr-nu site | Enable Astra firewall on the buildr-nu domain; run the initial vulnerability scan; fix any findings before public launch |
| **1Password** | Free 1 year + Developer Tools | Secrets management for the team: API keys (Stripe, Sentry, Datadog), deploy credentials, DB passwords | Create a shared 1Password vault called "Buildr Infrastructure"; store all service API keys there; use 1Password CLI to inject secrets into CI without hardcoding |
| **Dashlane** | Free Premium 6 months | Backup password manager for team members who prefer Dashlane | Set up Dashlane for personal credential management as a backup to 1Password for individual contributors |
| **Doppler** | Free Team subscription while student | Centralized secrets manager that syncs env vars across local dev, CI, staging, production | Create a Doppler project "buildr-nu" with environments (dev/staging/prod); migrate all `.env` values into Doppler; update CI to pull secrets from Doppler instead of GitHub Secrets |
| **Imgbot** | Free for all repos while student | Automatic image optimization on every PR (reduces page weight for buildr-nu and generated sites) | Install the Imgbot GitHub App on the buildrhel repo; it will auto-submit PRs that losslessly compress any images added to docs, templates, or generated workspaces |
| **Requestly** | Free Professional plan ($270 value) for 1 year | HTTP request interception and mocking for API development and testing in generated workspaces | Create a Requestly rule set that mocks the Stripe webhook responses during local development of payment-enabled workspaces; share the rule set with the team |
| **Polypane** | Free Individual plan for 1 year | Multi-viewport responsive design testing for buildr-nu and generated web apps | Open every generated workspace's deployed URL in Polypane; verify responsive behavior at 5 breakpoints; screenshot results as evidence for the evaluator |

---

## Tier 3: Development Tools

Services that accelerate building, improve developer experience, or aid workspace creation.

| Service | Free Offer | Buildr Use | Concrete One-Time Action |
|---------|-----------|------------|--------------------------|
| **JetBrains** | Free All Products subscription (annual renewal) | PyCharm for engine development, WebStorm for generated workspaces, DataGrip for MongoDB | Install PyCharm Professional; configure a run configuration for `pytest tests/` and a debug configuration for `forge_engine.py` with breakpoints at `_customize()` |
| **Visual Studio Code** | Free (coding packs for Java/Python/.NET) | Primary editor with Copilot integration; recommended in generated workspace ENTRY files | Install the Python coding pack; configure workspace settings (`.vscode/settings.json`) in the repo with recommended extensions: Python, Pylint, GitLens |
| **GitLens** | Free GitKraken Student Plan (6 months + 80% off) | Enhanced git blame, commit graph visualization, PR management inside VS Code | Install GitLens in VS Code; use the commit graph to visualize wave-based development branches; configure auto-linking to GitHub issues |
| **GitKraken** | Free Student Plan (6 months + 80% off) | Visual Git client for managing complex branching during parallel wave execution | Set up GitKraken with the buildrhel repo; create a workspace profile that shows all active wave branches side-by-side |
| **Tower** | Free Pro license while student | Alternative Git GUI for macOS users on the team | Configure Tower with the buildrhel repo; use its conflict resolution UI during parallel wave merges |
| **Termius** | Free Pro + Team while student | SSH client for managing DigitalOcean droplets from desktop and mobile | Add the DigitalOcean droplet as a saved host in Termius; configure SSH key auth; create command snippets for common deploy operations |
| **Notion** | Free Education plan with AI | Project management, meeting notes, roadmap tracking, team wiki for Buildr development | Create a Notion workspace with databases for: Feature Backlog (synced with `v2/improve.md`), Sprint Board, Decision Log (mirrors PREFLIGHT_DECISIONS pattern) |
| **Notion Template Collection** | Curated templates | Ready-made templates for project management and documentation | Import the "Engineering Wiki" template; customize it as the Buildr contributor handbook with links to CLAUDE.md, MANIFEST.md, and skill governance docs |
| **Bump.sh** | Free Standard plan ($149/mo) while student | Auto-generated API documentation from OpenAPI specs for Forge/Bridge engine APIs | Write an OpenAPI spec for the Bridge engine endpoints; connect Bump.sh to the repo; every push auto-updates live API docs at `bump.sh/buildr/doc/bridge-api` |
| **ToDiagram** | Free Pro plan (full editor, cloud storage) | Visualize preflight JSON artifacts, workspace orchestration.yaml, and agent-manifest.json as interactive diagrams | Upload `orchestration.yaml` from a generated workspace into ToDiagram; export an SVG of the wave dependency graph; embed it in the workspace's WORKSPACE.md |
| **PopSQL** | Free Premium while student | Collaborative SQL editor for querying MongoDB (via connector) or any SQL databases in generated workspaces | Connect PopSQL to the MongoDB Atlas instance; create saved queries for: "active preflight runs", "workspace generation success rate by week", "most-used vault items" |
| **SQLGate** | Free Standard for 1 year | Multi-database IDE for generated workspaces that use SQL backends (PostgreSQL, MySQL) | Set up SQLGate with connection profiles for the common databases used in generated workspaces; create template queries for the data models defined in CATEGORY_DATA_MODELS |
| **Deepnote** | Free Team plan while student | Collaborative notebooks for data analysis: vault item usage analytics, workspace generation metrics, preflight pass rates | Create a Deepnote project "Buildr Analytics"; build a notebook that reads discoveries.jsonl and plots: discoveries/week, topics distribution, engine performance trends |
| **Bootstrap Studio** | Free license while student | Rapid prototyping of buildr-nu landing page and UI components for generated workspaces | Design the buildr-nu landing page in Bootstrap Studio; export clean HTML/CSS; use it as the foundation template for the static-html workspace category |
| **Educative** | 6 months free (70+ courses) + 30% off | Team upskilling: Python, system design, web dev courses relevant to Buildr development | Complete the "System Design" and "Python for Developers" courses; apply learnings to improve Forge engine architecture |
| **FrontendMasters** | Free 6 months all courses | Deep JavaScript/React/Node training for building better generated workspace templates | Complete the "Full Stack" and "Design Systems" courses; use patterns learned to improve the NextJS workspace template quality |
| **Vaadin** | Free Pro subscription | Java-based progressive web app framework; alternative stack for generated workspaces | Add Vaadin as a supported stack option in Forge's STACK_FILE_MAPS; define file maps and module components for a Java-based booking workspace |
| **WorkingCopy** | Free Pro while student | Git client for iPad/iPhone; manage Buildr repo and review PRs from mobile | Configure WorkingCopy with the buildrhel repo; use it for on-the-go PR reviews of generated workspace code |
| **Xojo** | Free Pro license while student | Cross-platform desktop app development; potential stack for desktop-targeted generated workspaces | Add a minimal Xojo project template to Forge's scaffold options for the rare case of desktop app workspace generation |
| **GitHub Desktop** | Free (open source) | Simplified Git interface for contributors less comfortable with CLI | Document GitHub Desktop as the recommended Git client for new contributors in the repo's onboarding docs |

---

## Tier 4: Creative Leverage

Services with non-obvious but specific uses that unlock capabilities Buildr would not otherwise have.

| Service | Free Offer | Buildr Use | Concrete One-Time Action |
|---------|-----------|------------|--------------------------|
| **Zyte (Scrapy Cloud)** | 1 free forever unit, unlimited crawl time, 120-day retention | Automated intelligence gathering for the Scout skill: crawl Anthropic docs, competitor landing pages, trending GitHub repos, and framework changelogs on a schedule | Deploy a Scrapy spider to Zyte that crawls `docs.anthropic.com/changelog`, `github.com/trending`, and `nextjs.org/blog` daily; pipe results into `memory-system/continuum/discoveries.jsonl` via a webhook so Scout always has fresh external intelligence |
| **Testmail** | Free Essential plan while student | Automated end-to-end email testing for generated workspaces that include email features (auth, notifications, waitlist) | Create a Testmail namespace `buildr-test`; write a pytest fixture that sends email via the generated workspace's email service and asserts delivery/content via Testmail API; include this fixture in the workspace QA template |
| **ConfigCat** | 1000 feature flags, unlimited users, free | Feature flags for buildr-nu: gradual rollout of paid workspace generation, A/B test landing pages, toggle experimental Forge features | Create feature flags: `enable_paid_tier`, `enable_prescriptive_v2`, `enable_cross_vendor_execution`; wire ConfigCat SDK into buildr-nu backend; roll out features to 10% of users first |
| **Arduino Cloud** | Free 6 months + hardware discounts | IoT monitoring dashboard for the build server (a Mac): CPU temp, memory pressure, disk I/O, uptime; exposed as a live hardware health feed | Connect an Arduino board to the Mac build server via USB; push CPU temp, RAM usage, and uptime to Arduino Cloud every 60s; create a public dashboard widget embeddable in the buildr-nu status page |
| **Adafruit IO+** | Free 1 year + hardware discounts | Alternative/complementary IoT data platform: real-time feed of build server metrics with MQTT support, triggerable alerts | Set up Adafruit IO feeds for `forge-engine-runs`, `preflight-pass-rate`, `deploy-health`; create a trigger that sends a webhook alert when `forge-engine-runs` drops to zero for 2 hours (engine is stuck) |
| **Blockchair** | 100,000 free API requests | Blockchain timestamping of approved preflight artifacts for immutable proof of approval state at a point in time | After PREFLIGHT_APPROVAL.json status becomes `approved`, hash the file (SHA-256), submit an OP_RETURN transaction to Bitcoin testnet via Blockchair API, and store the tx hash in `PREFLIGHT_DECISIONS.json` as `blockchain_timestamp_tx` -- creates tamper-proof evidence of what was approved and when |
| **Camber** | 200 CPU hours/mo, 75GB storage, 200 LLM messages/mo | Scientific computing for vault-selector optimization: run Monte Carlo simulations on skill-selection algorithms, benchmark module-resolution performance at scale | Upload the vault-selector logic to Camber; run 10,000 simulated workspace-generation requests with randomized inputs; analyze which vault items are selected most/least; use results to prune or merge low-value vault items |
| **CARTO** | Free upgraded account for 2 years | Geographic visualization of buildr-nu users, generated workspace deployments, and market analysis for the commercial product | Connect CARTO to the MongoDB user/session data; create a map dashboard showing: where waitlist signups come from, which regions generate the most workspaces, geographic distribution of deployed apps -- use for targeted marketing decisions |
| **SimpleAnalytics** | Free Starter (100K pageviews/mo) for 1 year | Privacy-friendly analytics for buildr-nu (no cookies, GDPR-compliant) that tracks landing page conversion, docs engagement, and feature adoption without creepy tracking | Add the SimpleAnalytics script tag to the buildr-nu site and GitHub Pages docs; create goals for: "waitlist signup", "docs read > 3 pages", "workspace generation started"; use the data to optimize the landing page funnel |
| **Cryptolens** | 10 free licenses, unlimited end-users | License key management if buildr-nu sells workspace generation as a product: issue, validate, and revoke license keys programmatically | Create a Cryptolens product "Buildr Workspace Pro"; generate license keys that gate access to advanced preflight features; integrate the validation API into the buildr-nu backend so only licensed users can run prescriptive workspace generation |
| **DevCycle** | Free Starter (unlimited flags/seats) for 1 year | Advanced feature flag management with targeting rules: roll out experimental Forge features to specific user segments, run experiments on workspace quality | Create DevCycle flags for experimental engine features (e.g., `forge_parallel_module_resolution`, `imperfektum_personalized_memories`); target flags to beta users; measure workspace quality per variant |
| **POEditor** | Free Plus plan for 1 year | Localization management for buildr-nu UI and documentation; manage translations for the multilingual workspace module | Create a POEditor project for buildr-nu; import English strings; invite translators for Swedish, Spanish, German; auto-sync translated strings to the repo via GitHub integration so generated multilingual workspaces have real translations |
| **DailyBot** | Free Business plan (10 users, 6 months) | Automated async standups and retrospectives for the Buildr development team; integrates with Slack/Discord | Set up a DailyBot standup that runs every morning asking "What wave did you complete?", "What's blocking you?", "What discovery did you log?"; auto-post summaries to a `#buildr-standups` channel |
| **Visme** | Free Starter plan for 3 months | Create visual presentations and infographics: pitch decks for buildr-nu investors/partners, system architecture diagrams for docs, onboarding visual guides | Create a 10-slide pitch deck for buildr-nu: problem (LLMs guess), solution (layered build system), demo (workspace generation), traction (metrics from SimpleAnalytics), ask; export as PDF and embed in `docs/` |
| **Icons8** | Free 3 months (icons, photos, illustrations, music) | Design assets for buildr-nu landing page, generated workspace templates, and documentation illustrations | Download a consistent icon set for the buildr-nu UI (build, deploy, test, monitor, etc.); create an `assets/icons/` directory in the static-html template so generated websites ship with professional icons |
| **IconScout** | 60 premium icons/month for 1 year | Ongoing icon supply for generated workspace design systems | Download icons monthly matching the design-system token palette; add them to `vault/` as a shared resource that any generated workspace's design-system wave can reference |
| **Pageclip** | Free basic plan while student | Form backend for static sites: capture form submissions from generated static-html workspaces without server code | Add Pageclip as the default form handler in the static-html workspace template; configure it so any generated static website with a contact form works immediately on deploy without custom backend |
| **Appfigures** | Free analytics for 1 year | App store intelligence: if buildr-nu generates mobile apps, track their store rankings, reviews, and download trends | Connect Appfigures to any mobile app published from a generated workspace; create an automated weekly report of downloads and ratings; feed insights back as Scout discoveries |
| **SlideCoach** | 2,000 free credits (40 sessions) for 1 year | AI presentation coaching for pitching buildr-nu: practice investor pitches and get data-driven feedback on delivery | Upload the Visme pitch deck script to SlideCoach; practice 5 times; iterate on pacing and clarity based on AI feedback; record the final version as the canonical pitch |
| **Themeisle (Neve)** | Free Neve Agency WordPress theme for 1 year | WordPress theme for the buildr-nu blog or marketing site if WordPress is chosen as the CMS | Install Neve Agency on a WordPress instance; customize it with Buildr branding; publish blog posts about workspace generation, agent orchestration, and vault items to build SEO authority |

---

## Tier 5: Low/No Relevance

Listed for completeness. These are learning platforms, career tools, community programs, or niche services with no actionable integration point for Buildr.

| Service | Why Tier 5 |
|---------|-----------|
| **Codedex** | Learn-to-code platform for beginners; no integration surface for Buildr |
| **DataCamp** | Data science courses; educational only, no tool/API to integrate |
| **Scrimba** | Interactive frontend courses; educational only |
| **Thinkful** | 1-month web dev course access; educational only |
| **GoRails** | Ruby/Rails tutorials; Buildr is Python-based, no Rails workspaces currently |
| **SymfonyCasts** | Symfony/PHP tutorials; not relevant to Buildr's stack |
| **AlgoExpert** | Interview prep platform; no system integration |
| **InterviewCake** | Interview prep; no system integration |
| **GitHub Certification Offer 2025** | Exam voucher; team credentialing, not a tool |
| **GitHub Community Exchange** | Student community portal; no API or integration surface |
| **GitHub Campus Experts** | Community leadership program; no tool to integrate |
| **OpenSauced** | Acquired/deprecated; limited remaining functionality |
| **Octicons** | Open-source icon library (already free for everyone); use Icons8/IconScout for premium assets instead |
| **HazeOver** | macOS focus app (dims background windows); personal productivity, no system integration |
| **PomoDone** | Pomodoro timer; personal productivity, no system integration |
| **Microsoft Azure (ages 13-17)** | Subset of Azure for younger students; use the main Azure offer instead |
| **Microsoft Visual Studio Dev Essentials** | Overlaps with Azure + VS Code offers already listed; no unique integration |

---

## Service Count Verification

| Tier | Count |
|------|-------|
| Tier 1: Direct Infrastructure | 14 |
| Tier 2: Quality & Observability | 18 |
| Tier 3: Development Tools | 20 |
| Tier 4: Creative Leverage | 20 |
| Tier 5: Low/No Relevance | 17 |
| **Total** | **89** |

Every service from the GitHub Student Developer Pack appears in exactly one tier.
