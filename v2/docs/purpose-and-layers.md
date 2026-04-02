# Buildr — syfte, lager och agentförståelse

> **Spegel:** samma innehåll finns under `docs/BUILDR-purpose-and-layers.md`. Uppdatera båda vid ändringar.

## Existensberättigande (bredare än “workspace som bygger produkt”)

Buildr är ett **lagerbyggt system** där en **prompt eller projektbeskrivning** startar ett flöde och en agent **systematiskt sätter ihop** det som behövs för användarens syfte: lösa problem, automatisera steg för steg, skapa något som kan vara internt eller **säljbart**, osv.

**Workspace** är det **verktyg och den bärare** (vågor, state, kontrakt, QA, roller) som gör att en agent kan **exekvera pålitligt** utan att uppfinna processen varje gång. Workspace är **inte** själva definitionen av systemet — det är den **bästa etablerade idén** för att leverera det syftet i agentmiljöer.

**v2-preflight** tillför: innan workspace skapas kan **syfte, risker, minimal arkitektur, acceptance och beslut** frysa och (delvis) valideras — så leveransen spårar tillbaka till avsikten, inte bara till en scaffold.

**Prescriptive workspace generation** (v2 Fas 1–6) tillför: workspace-innehållet är inte längre berättande utan **algoritmiskt**. Varje modul specificerar exakta filer, datamodeller, komponent-props, steg-för-steg-flöden och stabila acceptanskriterier. En agent behöver inte gissa — den följer instruktionerna.

---

## Två sätt att uppfylla syfte: specifikt och strukturellt

Ett syfte kan uppfyllas genom **både** konkreta leveranser **och** strukturer som gör framtida leveranser möjliga. En agent ska kunna skilja på dem och föreslå båda när det passar.

| Typ | Vad det är | Exempel |
|-----|------------|---------|
| **Specifikt** | Något namngivet, mätbart eller direkt användbart | Ett API-kontrakt, en betalningsväg, en feature-flagga, en migrationsfil, en checklista med pass/fail, en modul i workspace |
| **Strukturellt** | Ramar som gör rätt saker enkla och fel saker svåra | Ny eller uppdaterad **vault**-skill/constraint/strategi, preflight-fält som låser CRI, **improve**-backlog-punkt, Forge-hook, rutin som körs före generering, tydlig tvåvägs-path (legacy vs advanced) |

**Poäng:** samma användarprompt kan kräva *först* strukturella bitar (så nästa workspace blir rätt) och *sedan* specifika implementationer i ett workspace. Agenten ska **inte** alltid välja “bara generera workspace” om syftet lika väl uppfylls genom att **förstärka repot** (inom `docs/skill-governance.md` och befintliga processer: Smith, Scout, improve).

---

## Agentens mandat att föreslå vad som är möjligt

En agent som arbetar i detta repo ska **aktivt** kunna:

1. **Kartlägga** vad som redan möjliggörs (läs lager-dokumentationen nedan).
2. **Skilja** “redan stöds” från “saknas men lågt hängande” från “kräver större ingrepp”.
3. **Föreslå** konkreta åtgärder: nya vault-items, en rad i `v2/improve.md`, en preflight `required_missing_inputs`, ett test, en operator-/mall-justering — med **tydlig koppling till användarens syfte**.
4. **Respektera** godkännandegrindar: vault/smith enligt `docs/skill-governance.md`; system skills bara när det är motiverat; inga hemliga hopp över `approved` preflight i advanced-flödet.

Förslag ska vara **handlingsbara** (vad som ska skrivas, var filen ska ligga, vilken binär effekt det får), inte bara allmän uppmuntran.

---

## Vad `v2/start.md` och `v2/improve.md` gjort (och varför)

| Artefakt | Roll |
|----------|------|
| **`v2/start.md`** | Bootstrap för en **tom** session som ska **författa** v2-artefakter enligt `v2/claude.md`: läsordning, hårda regler, `AUTHOR_GATE`, valfritt steg mot `improve.md` efter PASS. **Varför:** reproducerbar, grindad författning utan glömda krav. |
| **`v2/improve.md`** | Backlog för **grundrepot** kring preflight (validering, ingest, operator, mallar, vault, git, docs) + **risktabell** och **sanity-check**. **Varför:** v2-skillen räcker inte om motor, mallar och discoverability inte följer med. |

---

## Utöver start/improve (i repot)

- Utökad **`v2/claude.md`** (commercial-grade krav, author gate, governance-länk).
- **`skills/buildr-operator/SKILL.md`**: avsnitt **Two entry paths** (legacy vs advanced) + länkar till preflight-ingest, validator, overview, vault-rutin.
- **`tests/test_preflight_validate.py`** + **`MANIFEST.md`**: regression på v1.5-grinden.
- **Korskopplingar** mellan `v2/improve.md`, `integration-with-operator`, workspace-architect `SKILL.md`.

---

## Fas 1–6: Prescriptive Workspace Generation (vad som gjordes)

Sex faser transformerade workspace-generering från **berättande** till **prescriptiv** — genererade workspaces innehåller nu tillräckligt med detalj för att agenter kan exekvera autonomt.

### Fas 1: Algoritmiska modulspecar

**Problem:** `ModuleSpec` hade fälten `files_to_create`, `data_model`, `user_flows`, `components` — alla tomma. Modulspecar sa "Booking Calendar: Date/time selection, availability display, booking flow. Bygg modulen."

**Lösning:** Fyra nya statiska diktioner i `ModuleResolver` (`engines/forge_engine.py`):

| Dict | Mappning | Exempel |
|------|----------|---------|
| `STACK_FILE_MAPS` | (stack, modul-id) → filsökvägar | `("nextjs", "booking-calendar")` → 11 namngivna filer |
| `CATEGORY_DATA_MODELS` | (kategori, modul-id) → entitetsscheman | `Booking {id, service_id, date, time_slot, status, ...}` |
| `DETAILED_USER_FLOWS` | (kategori, modul-id) → 10–20-stegsflöden | 14-stegs bokningsflöde med API-anrop och felhantering |
| `MODULE_COMPONENTS` | (stack, modul-id) → komponentnamn med props | `DatePicker (availableDates[], selectedDate, onSelect, ...)` |

**`_customize()`** populerar varje `ModuleSpec` från diktionerna vid workspace-generering. **`_render_module()`** renderar nya sektioner: "Filer att skapa", "Datamodell", "Komponenter", "Användarflöde (steg-för-steg)".

**Stabila acceptanskriterium-ID:n:** Varje kriterium får ett ID (`AC-BOOKING_CALENDAR-01`) som refereras av evaluator, gates och kontrakt.

**Täckning:** NextJS (booking, e-commerce, web-app, website), static-html (website), python-fastapi (API/tool). Alla kärnmoduler för dessa kategorier har prescriptiva data.

### Fas 2: Konkreta waves och kontrakt per modul

**Problem:** Bara `waves/001-foundation.md` genererades. Övriga moduler hade ingen wave. Kontrakt var stubs med "shared truth"-placeholder.

**Lösning:**

- **En wave per modul.** Ny metod `_render_wave_for_module()` genererar en wave med imperatiska steg (`1. Create src/components/booking/DatePicker.tsx — implement per module spec`), tier, beroenden, agent-tilldelning och parallell-gruppinformation.
- **Ett kontrakt per modul.** Ny metod `_render_contract_for_module()` genererar kontrakt med faktiska interfaces: dataentiteter med fälttyper, komponent-props, API-endpoints härledda från filstrukturen.
- **`orchestration.yaml`** registrerar alla waves (inte bara 001) med `version: 2`.
- **Parallella exekveringsfaser.** Ny metod `_compute_build_phases()` grupperar moduler utan ömsesidiga beroenden i parallella faser. Resultatet skrivs till `parallel_phases:` i `orchestration.yaml`.

**Resultat (booking-workspace):** 9 waves, 9 kontrakt, 6 parallella faser (fas 3 kör booking-catalog + multilingual + seo + whatsapp samtidigt).

### Fas 3: Strukturerad evaluator-feedback

**Problem:** Evaluatorn skrev fritext. Buildern kunde inte parsa "The booking calendar shows all dates but I can't see which are available" till konkret åtgärd.

**Lösning:** Uppdaterad `templates/EVALUATOR.md` med obligatoriskt YAML-frontmatter-format:

```yaml
---
wave: "004-booking-calendar"
verdict: PASS
blocker_count: 0
should_fix_count: 1
---
```

Följt av AC-ID-verifiering (`AC-BOOKING_CALENDAR-01: PASS`, `AC-BOOKING_CALENDAR-03: FAIL (SHOULD_FIX) — missing loading state`). Varje FAIL inkluderar severity och filsökväg. Buildern kan parsa detta mekaniskt.

Gate 2 i `templates/qa/gates.md` refererar nu AC-ID:n och kräver evaluator-feedback-fil.

### Fas 4: Cross-vendor agentteam

**Problem:** Allt antog Claude Code. Codex- eller Gemini-agenter hade ingen entry-point.

**Lösning:** Tre nya templates:

| Fil | Vendor | Nyckelinformation |
|-----|--------|-------------------|
| `ENTRY-claude.md` | Anthropic (Claude Code) | Sub-agent-spawning via Agent-tool, opus/sonnet/haiku-mapping |
| `ENTRY-codex.md` | OpenAI (Codex CLI) | o3/o4-mini-mapping, parallellisering via separata terminaler |
| `ENTRY-gemini.md` | Google (Gemini CLI) | 2.5-pro/2.5-flash-mapping, multi-vendor parallellstrategi |

Varje fil: (1) pekar till `RUN.md` som kanonisk exekveringsloop, (2) mappar abstrakta capabilities till vendor-specifika verktyg, (3) definierar modelltier-mappning, (4) förklarar hur parallella waves hanteras i den vendorn.

`ScaffoldGenerator.generate()` producerar automatiskt alla tre entry-filer. `CLAUDE.md` refererar dem under "Cross-Vendor Agents".

**Multi-vendor-parallellisering:** Oberoende waves i samma fas kan köras av olika vendors i separata terminaler. Exempel fas 3: Claude → booking-catalog, Gemini → multilingual, Codex → seo, Claude → whatsapp.

### Fas 5: Vault enrichment

Fyra nya vault-items inom radgränser:

| Item | Typ | Syfte |
|------|-----|-------|
| `implementation-playbook.md` | Skill | Steg-för-steg: modulspec → fungerande kod (12 steg + vanliga misstag) |
| `contract-authoring.md` | Skill | Hur man skriver och underhåller interface-kontrakt (6 steg) |
| `parallel-wave-execution.md` | Strategi | När/hur parallella waves körs (4 steg + fallgropar) |
| `wave-parallel-merge.md` | Rutin | Verifiering efter parallella waves (6 binära checks) |

Nyckelord tillagda i `engines/vault_selector.py` ("implementation" → playbook, "contract" → authoring).

### Fas 6: End-to-end-tester

**19 nya tester** i `tests/test_end_to_end.py`:

- `TestPrescriptiveModules` (5 tester): Verifierar att booking- och webapp-moduler har populerade `files_to_create`, `data_model`, `user_flows`, `components`.
- `TestBuildPhases` (4 tester): Parallella faser existerar, foundation först, deploy sist, alla moduler representerade.
- `TestWorkspaceGeneration` (10 tester): Fullständig workspace genereras → varje modul har wave + kontrakt, kontrakt har riktigt innehåll (inte placeholders), orchestration.yaml har alla waves + parallel_phases, waves har imperatiska steg, AC-ID:n i moduler, entry-filer existerar, agent-manifest korrekt, evaluator har strukturerat format.

**Total testsvit:** 51 tester (32 befintliga + 19 nya), alla passerar.

---

## Möjligt vs delvis möjligt (uppdaterat efter Fas 1–6)

**Möjligt nu:**
- Strukturerat flöde prompt → preflight → godkänd staging → workspace → executor.
- Prescriptiva modulspecar: agent vet exakt vilka filer, datamodeller, komponenter och flödessteg som ska skapas.
- Konkreta waves med imperatiska steg och agent-tilldelning.
- Kontrakt med riktiga interfaces (dataentiteter, API-endpoints, komponent-props).
- Parallell exekvering: oberoende waves körs simultant av samma eller olika vendors.
- Cross-vendor: Claude, Codex och Gemini kan arbeta på samma workspace med entry-filer som mappar deras verktyg.
- Strukturerad evaluator-feedback: parsbar av builder med AC-ID-verifiering.
- Spårbara artefakter; validering av filer och approval-payload; återanvänd vault.
- 51 tester som verifierar hela kedjan.

**Delvis möjligt (kvarvarande gap):**
- Garanterad perfekt förståelse av syfte (preflight är **frysning vid approval**, inte sanningsteorem).
- Full kod-tvång överallt (v1 är prompt-enforced; Forge/Bridge-hook är backlog).
- “Byrånivå utan människa” — systemet höjer golvet kraftigt men ersätter inte all domän- och säkerhetsbedömning.
- Enhancement-moduler (whatsapp, seo, deploy) har ännu inte filkartor för alla stacks — agent får generisk guidance. Kärnmoduler (foundation, design-system, auth, booking, e-commerce, dashboard, data-management, payment) är fullt prescriptiva.
- Imperfektum-minnen är hårdkodade per kategori — personalisering per modul-innehåll är backlog.
- Vault-items saknar `integration_snippet` för automatisk applicering i specifika modulsteg — agenten läser skillen och applicerar manuellt.

---

## Hur en agent bygger förståelse “i kvadrat”

Målet: kunna svara på **(A)** vad repot möjliggör per lager, **(B)** vad användarens syfte kräver i operativa termer, och **(C)** vilken **komposition** (skills, vault, preflight, workspace, förbättringar i repo) som binder ihop A och B.

1. **Konstitution:** `BUILDR_ARCHITECTURE.md`, `MANIFEST.md`, `README.md`, `docs/skill-governance.md`.
2. **Roller:** operator, executor, smith, scout, rescue, workspace-architect, advanced operator-prompt (`v2/prompts/…`).
3. **Körkedja:** `docs/v2-overview.md`, `skills/buildr-operator/references/preflight-ingest.md`, `vault/routines/preflight-gate-check.md`.
4. **Maskinell sanning:** `engines/preflight_validate.py`, `preflight-handoff.schema.json`, `docs/workspace-from-preflight.md`.
5. **Backlog / gap:** `v2/improve.md`.
6. **Översätt syfte → komposition:** välj path (advanced/legacy), preflight vid behov, vault-sats, acceptance, ev. repo-förstärkning **innan** eller **vid sidan av** workspace.

**Kvadrat** = A × B × C medvetet kopplade, inte bara “skapa en mapp”.

---

## Vad en genererad workspace nu innehåller

```
my-project/
├── CLAUDE.md                    ← Orkestreringsprotokoll + cross-vendor-referens
├── ENTRY-claude.md              ← Entry: Claude Code (sub-agenter, opus/sonnet)
├── ENTRY-codex.md               ← Entry: Codex CLI (o3/o4-mini, parallella terminaler)
├── ENTRY-gemini.md              ← Entry: Gemini CLI (2.5-pro/flash)
├── AGENT.md                     ← Builder-beteende + läsordning + execution gate
├── EVALUATOR.md                 ← Strukturerad feedback (YAML + AC-ID-verifiering)
├── RUN.md                       ← 20-stegs exekveringsloop
├── PROJECT.md                   ← Hårda constraints + modulöversikt
├── SYSTEM.md                    ← Designsystem + kodstandarder
├── MEMORY.md                    ← Imperfektum: fabricerade erfarenheter
├── WORKSPACE.md                 ← Master-översikt
├── TOOLS.md                     ← Tillgängliga verktyg (Index-urval)
├── spec.json                    ← Maskinläsbar projektspec
│
├── agents/                      ← Rollbaserat agentteam (deriverat från kategori)
│   ├── agent-manifest.json         Roster: namn, roll, modell, routing, rapporterar-till
│   ├── orchestrator.md             Opus: delegerar, aldrig kodar
│   ├── platform-lead.md            Opus: domänarkitektur
│   ├── ui-builder.md               Sonnet: frontend-implementation
│   ├── api-builder.md              Sonnet: backend-implementation
│   ├── qa-lead.md                  Sonnet: skeptisk review, pass/fail
│   └── deploy-agent.md             Haiku: deploy/CI/CD
│
├── state/orchestration.yaml     ← Alla waves + parallel_phases + budget
│
├── waves/                       ← EN WAVE PER MODUL (imperatiska steg)
│   ├── 001-foundation.md           13 filer, tier A, agent: platform-lead
│   ├── 002-design-system.md        12 filer, 11 komponenter, tier A
│   ├── 003-booking-catalog.md      8 filer, 1 datamodell, 8-stegs flöde
│   ├── 004-booking-calendar.md     11 filer, 2 datamodeller, 14-stegs flöde
│   ├── 005-payment.md              8 filer, 1 datamodell, 10-stegs flöde
│   └── ...
│
├── contracts/                   ← ETT KONTRAKT PER MODUL (riktiga interfaces)
│   ├── foundation.md               Stack, kategori, locked decisions
│   ├── booking-calendar.md         Booking {10 fält}, Availability {3 fält}, API-endpoints
│   └── ...
│
├── modules/                     ← PRESCRIPTIVA MODULSPECAR
│   ├── 01-foundation.md            Filer, implementation-steg
│   ├── 04-booking-calendar.md      11 filer, 2 datamodeller, 5 komponenter, 14-stegs flöde, 5 AC-ID:n
│   └── ...
│
├── qa/
│   ├── gates.md                    3-fas: concept → implementation (med AC-ID) → delivery
│   ├── checklist.md                Per-modul binära checks
│   ├── acceptance.md               Projektomfattande acceptanskriterier
│   └── evaluations/latest.md       YAML-frontmatter + AC-verifiering
│
├── vault-selection/              ← Vault-items valda för detta projekt
│   ├── skills/, constraints/, routines/, memories/
│   └── 001-foundation.json
│
└── onboarding/prompt.md          ← Om onboarding inte är klar
```

---

## Snabb pekare för nya sessioner

- V2-författning: `v2/start.md`
- Grundrepo efter v2: `v2/improve.md`
- Syfte/lager/förslag: `docs/BUILDR-purpose-and-layers.md` (**denna fil:** `v2/docs/purpose-and-layers.md`)
- Prescriptive generation (Fas 1–6): se sektion ovan + `engines/forge_engine.py` (STACK_FILE_MAPS, CATEGORY_DATA_MODELS, etc.)
- Cross-vendor: `templates/ENTRY-claude.md`, `templates/ENTRY-codex.md`, `templates/ENTRY-gemini.md`
- Parallell exekvering: `vault/strategies/parallel-wave-execution.md`, `orchestration.yaml` → `parallel_phases`
- End-to-end-tester: `tests/test_end_to_end.py` (19 tester)
