# Architecture Decisions

> All agents MUST respect decisions here. Decisions are LOCKED once recorded.
> To change a decision: add a NEW entry that supersedes the old one with rationale.

## Format
### [Date] — [Decision Title]
**Context:** Why this decision was needed
**Choice:** What was decided
**Alternatives considered:** What was rejected and why
**Consequences:** What this enables and constrains

## Decisions
<!-- Append-only. Newest at bottom. -->
# Architecture Decisions

> All agents MUST respect decisions here. Decisions are LOCKED once recorded.
> To change a decision: add a NEW entry that supersedes the old one with rationale.

## Format
### [Date] — [Decision Title]
**Context:** Why this decision was needed
**Choice:** What was decided
**Alternatives considered:** What was rejected and why
**Consequences:** What this enables and constrains

## Decisions
<!-- Append-only. Newest at bottom. -->
# ARCHITECTURE DECISIONS

> Skrivs av Architect. Alla agenter MÅSTE respektera beslut här.

## Beslut:

### 2026-03-12 — Stack: Next.js 15 + TypeScript + Tailwind + Prisma + Vitest
Kontext: SEO-analysverktyg som webbapp, fullstack.
Val: Next.js 15 App Router, TypeScript strict, Tailwind CSS, PostgreSQL + Prisma, Vitest.
Alternativ: Express+React (mer boilerplate), Remix (mindre ekosystem), Jest (långsammare).
Konsekvenser: App Router med Route Handlers, Prisma-genererade typer, server-side crawler.

### 2026-03-12 — Crawler: Cheerio + native fetch (ingen headless browser)
Kontext: Behöver parsa HTML för SEO-analys.
Val: Cheerio för HTML-parsning, native fetch med timeout.
Alternativ: Puppeteer (tungt, behöver Chrome), jsdom (långsammare).
Konsekvenser: Kan inte analysera SPA-sidor som kräver JS-rendering. Acceptabelt per scope.

### 2026-03-12 — Ingen autentisering
Kontext: Projektbeskrivningen nämner inte auth, scope-begränsning.
Val: Publikt API utan auth.
Alternativ: NextAuth (overhead för MVP).
Konsekvenser: Alla endpoints publika. Auth kan läggas till senare som feature.

### 2026-03-12 — Service-lager mellan API-routes och Prisma
Kontext: Undvika att lägga affärslogik i route handlers.
Val: src/lib/services/ med en service per domän.
Alternativ: Direkt Prisma i routes (snabbare, men svårtestat och ostrukturerat).
Konsekvenser: Testbarhet, separation of concerns, enklare att mocka.

### 2026-03-12 — Analyzer-arkitektur: en fil per SEO-kategori
Kontext: 6 SEO-kategorier att analysera, varje med egen logik.
Val: src/lib/analyzers/ med en modul per kategori, gemensamt interface.
Alternativ: En stor analyze-funktion (ohanterligt), plugin-system (over-engineering).
Konsekvenser: Enkelt att lägga till nya kategorier. Varje analyzer tar HTML → { score, issues[] }.
