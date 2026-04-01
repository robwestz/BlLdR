# Buildr — syfte, lager och agentförståelse

> **Spegel:** samma innehåll finns under `v2/docs/purpose-and-layers.md` (v2-mappen). Uppdatera båda vid ändringar.

## Existensberättigande (bredare än “workspace som bygger produkt”)

Buildr är ett **lagerbyggt system** där en **prompt eller projektbeskrivning** startar ett flöde och en agent **systematiskt sätter ihop** det som behövs för användarens syfte: lösa problem, automatisera steg för steg, skapa något som kan vara internt eller **säljbart**, osv.

**Workspace** är det **verktyg och den bärare** (vågor, state, kontrakt, QA, roller) som gör att en agent kan **exekvera pålitligt** utan att uppfinna processen varje gång. Workspace är **inte** själva definitionen av systemet — det är den **bästa etablerade idén** för att leverera det syftet i agentmiljöer.

**v2-preflight** tillför: innan workspace skapas kan **syfte, risker, minimal arkitektur, acceptance och beslut** frysa och (delvis) valideras — så leveransen spårar tillbaka till avsikten, inte bara till en scaffold.

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

## Möjligt vs delvis möjligt

**Möjligt:** Strukturerat flöde prompt → preflight → godkänd staging → workspace → executor; spårbara artefakter; validering av filer och approval-payload; återanvänd vault; successiv förbättring via improve och tester.

**Delvis möjligt:** Garanterad perfekt förståelse av syfte (preflight är **frysning vid approval**, inte sanningsteorem); full kod-tvång överallt (v1 är prompt-enforced; Forge/Bridge-hook är backlog); “byrånivå utan människa” (systemet höjer golvet kraftigt men ersätter inte all domän- och säkerhetsbedömning).

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

## Snabb pekare för nya sessioner

- V2-författning: `v2/start.md`
- Grundrepo efter v2: `v2/improve.md`
- Detta dokument (syfte/lager/förslag): du läser det nu; v2-kopia: `v2/docs/purpose-and-layers.md`
