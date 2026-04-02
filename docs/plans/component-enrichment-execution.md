# Component Enrichment — vad som måste fungera och varför

Du läser detta för att du ska bygga det som gör att Buildr producerar workspaces där agenter kan exekvera autonomt. Om du efter att ha läst klart inte förstår varför varje del existerar, läs om. Om en del inte har ett tydligt varför — den hör inte hit.

---

## Syftet (det enda som får planeras)

En användare beskriver ett projekt. Buildr kör preflight och producerar arkitekturkomponenter (COMP-001 genom COMP-N). Dessa komponenter blir moduler i ett workspace. **Modulerna måste innehålla tillräckligt konkreta steg för att en agent som aldrig sett projektet kan följa dem till färdigt resultat.**

Det är syftet. Allt annat i detta dokument existerar för att det ska fungera.

Inte "fungera en gång" — fungera varje gång, för alla projekttyper, reproducerbart. En bokningssajt och en macOS-plattformssetup ska gå genom samma process och producera lika detaljerade moduler.

---

## Varför detta inte fungerar idag

Läs detta innan du kodar. Om du inte förstår varför det är trasigt förstår du inte vad du fixar.

**Problemet i en mening:** Enrichment matchar vault-items via nyckelord, men nyckelorden är för breda — ett infrastrukturprojekt ("OpenClaw Core") får REST API-designsteg från `api-design.md` istället för installations-kommandon.

**Varför nyckelordsmatchning inte räcker:**

Vault selector söker ord i komponentens beskrivning. "OpenClaw Core" → beskrivningen nämner "gateway", "API", "daemon" → vault returnerar `api-design.md` (matchar "API"), `error-boundary.md` (matchar brett) → enrichment extraherar "Choose HTTP method: GET/POST/PUT..." som implementeringssteg.

Resultatet: en agent som ska installera OpenClaw med `npm install -g openclaw@latest && openclaw onboard` får istället instruktioner om REST-endpoints. **Stegen hör till fel domän.** Vault-matchningen ger falsk precision.

**Varför generiska fallback-steg inte räcker:**

När ingen vault matchar produceras: "Research: determine exact setup steps for macOS User Isolation." Det är en instruktion att researcha, inte ett resultat av research. En autonom agent behöver `System Settings → Users & Groups → Add User → namn: openclaw → typ: Standard`, inte "ta reda på hur man gör detta."

**Varför detta inte är ett vault-coverage-problem:**

Fler vault items löser inte kärnan. Problemet är att enrichment inte skiljer mellan "denna vault skill handlar om SAMMA SAK som komponenten" och "denna vault skill råkar matcha ett nyckelord i komponentens beskrivning." `api-design.md` matchar nyckelordet "API" i "OpenClaw Core — REST API gateway daemon" — men komponenten handlar om att INSTALLERA en gateway, inte DESIGNA ett API.

---

## Vad som måste vara sant för att syftet uppfylls

Fem saker. Om alla fem är sanna fungerar enrichment. Om en saknas fungerar det inte.

### 1. Vault-matchning måste skilja relevans från nyckelordsträff

**Varför:** En vault skill som matchar ett nyckelord men handlar om en annan domän ger felaktiga steg. Falska positiver är värre än inga matchningar — de producerar moduler som ser prescriptiva ut men leder agenten fel.

**Vad som ska vara sant:** När enrichment matchar en vault skill mot en komponent, ska det finnas ett test: "Handlar denna vault skill om SAMMA TYP AV UPPGIFT som komponenten?" Installation av en daemon ≠ design av ett REST API, även om båda nämner "API."

**Hur du vet att det fungerar:** Kör enrichment på OpenClaw-projektet. Komponenten "macOS User Isolation" ska INTE få steg från `api-design.md`. Komponenten "OpenClaw Core" ska matcha `deploy-checklist.md` (installation) eller `environment-config.md` (konfiguration), inte `api-design.md` (designmönster).

### 2. Icke-matchade komponenter måste producera konkreta steg, inte research-instruktioner

**Varför:** En autonom agent som läser "Research: determine exact setup steps" staller. Den har ingen webåtkomst, eller om den har det vet den inte VAD den ska söka efter. Enrichment måste producera steg, inte uppdrag att hitta steg.

**Vad som ska vara sant:** Varje komponent har minst 3 implementation_steps som är konkreta handlingar (kommandon, UI-åtgärder, filskapande). Acceptance criteria från preflight innehåller redan test-procedurer (pass-villkor) — dessa SKA extraheras som steg, inte bara som verifiering.

**Hur du vet att det fungerar:** Varje modul i det genererade workspacet har en "Användarflöde"-sektion med steg som en agent kan följa utan att behöva researcha först. Stegen kommer från (a) preflight acceptance criteria pass-conditions, (b) komponentens sub_components om de finns i arkitekturen, eller (c) vault skills som faktiskt matchar domänen.

### 3. Preflight-arkitekturen måste vara informationskällan för steg, inte bara för komponentnamn

**Varför:** Preflight-artefakterna innehåller redan detaljerad information som enrichment inte använder idag. `PREFLIGHT_ARCHITECTURE.json` har `sub_components` per komponent (t.ex. "Separate home directory /Users/openclaw", "Separate Keychain", "Standard non-admin permissions"). `PREFLIGHT_ACCEPTANCE.json` har `pass_condition` med konkreta testprocedurer. Denna data ÄR implementeringssteg — enrichment bara extraherar dem inte.

**Vad som ska vara sant:** Enrichment läser `sub_components` från arkitekturen och `pass_condition` från acceptance criteria. Sub-components blir implementation_steps. Pass-conditions blir verifieringssteg. Om detta ger ≥3 steg per komponent behövs ingen vault-matchning alls — preflight redan levererade HOW.

**Hur du vet att det fungerar:** Modulen "macOS User Isolation" får steg som "Create separate home directory /Users/openclaw", "Create separate Keychain", "Set Standard non-admin permissions" — direkt från preflight-arkitekturen, inte från vault.

### 4. Vault-matchning ska vara ett KOMPLEMENT, inte primärkällan

**Varför:** Preflight researchar projektet. Vault innehåller generiska mönster. Preflight-specifik data > generisk vault-data. Men vault tillför värde när preflight inte specificerade HOW (t.ex. "hur konfigurerar man en launchd-plist" — preflight sa bara "use launchd").

**Vad som ska vara sant:** Enrichment prioriterar (i denna ordning):
1. Preflight `sub_components` → implementation steps
2. Preflight acceptance `pass_condition` → verification steps
3. Vault skills som matchar komponentens UPPGIFTSTYP (inte bara nyckelord)
4. Generisk fallback BARA om 1-3 ger < 3 steg

**Hur du vet att det fungerar:** En komponent med rika sub_components i preflight får INGA vault-steg — den har redan tillräckligt. En komponent utan sub_components (t.ex. "Security Hardening" med bara ett namn och justification) FÅR vault-steg från `environment-config.md` eller liknande.

### 5. Forge-skräp i PROJECT.md ska inte finnas när preflight styr

**Varför:** PROJECT.md visar "Kategori: booking", "Stack: nextjs", "Designsystem: #18181B, Inter, square buttons" för ett infrastrukturprojekt. Agenten läser detta och tror den bygger en webapp. CRI-sektionen i botten av filen är korrekt men topphalvan motverkar den.

**Vad som ska vara sant:** När preflight finns ska PROJECT.md reflektera preflightens data, inte forges kategori-klassificering. Projektbeskrivning, målgrupp, och constraints ska komma från CRI. Teknisk stack, designsystem, och kategori ska antingen härledas från preflight-arkitekturen eller utelämnas.

**Hur du vet att det fungerar:** PROJECT.md för OpenClaw-projektet nämner INTE "booking", INTE "nextjs", INTE CSS-färger. Den nämner "macOS platform setup", "Node.js runtime", "OpenClaw gateway daemon."

---

## Vad som ska ändras (och ingenting annat)

Varje ändring nedan löser exakt ett av de fem kraven ovan. Om en ändring inte löser ett krav hör den inte hit.

### Ändring A → Löser krav 3 och 4 (preflight som primärkälla)

Skriv om `PreflightIngestor.enrich_modules()` i `engines/bridge.py`.

Ny logik:
```
För varje modul:
  1. Hämta komponentens sub_components från PREFLIGHT_ARCHITECTURE.json
  2. Varje sub_component → ett implementation_step
  3. Hämta acceptance criteria som matchar denna modul
  4. Varje pass_condition → ett verification_step
  5. Om steg < 3: KÖR vault-matchning (befintlig logik, men med relevans-test per ändring B)
  6. Om steg fortfarande < 3: generisk fallback
```

### Ändring B → Löser krav 1 (relevans vs nyckelord)

I enrichment-logiken, efter vault_selector returnerar matchningar: filtrera bort vault skills vars DOMÄN inte matchar komponentens UPPGIFTSTYP.

Enklaste implementationen: vault skills har en implicit domän baserad på sin fil-path (skills/api-design = "api-design", skills/deploy-checklist = "deploy"). Komponenter har en uppgiftstyp som kan härledas:
- Om komponentens beskrivning nämner "install", "setup", "configure", "create user" → uppgiftstyp = "infrastructure/setup"
- Om den nämner "API", "endpoint", "route" utan "install"/"setup" → uppgiftstyp = "api-design"
- Om den nämner "UI", "component", "page", "form" → uppgiftstyp = "frontend"

En vault skill matchar RELEVANT om dess domän överlappar med komponentens uppgiftstyp. `api-design.md` matchar "api-design" men inte "infrastructure/setup".

### Ändring C → Löser krav 5 (clean PROJECT.md)

I `bridge.py` `_apply_preflight_to_workspace()`: om preflight finns, skriv om PROJECT.md-sektionerna som forge genererade.

Ersätt:
- "Kategori: booking" → Ta bort eller ersätt med preflight-klassificering
- "Stack: nextjs" → Ersätt med "Stack: determined by architecture" eller utelämna
- "Designsystem"-sektionen → Ta bort (infrastrukturprojekt har inget designsystem)
- "Deriveringslogg" → Behåll CRI-constraints, ta bort forge-specifika deriveringar

---

## Verifiering (hur du vet att syftet uppfylls)

Kör dessa två test. Om båda passerar är syftet uppfyllt.

**Test 1: OpenClaw (infrastruktur med preflight)**
```
python -m engines.bridge --description "Secure OpenClaw platform on MacBook Air M2" \
  --preflight v2/.buildr/preflight/openclaw-macbook-platform --out .tmp/verify-infra
```
Verifiera:
- [ ] Modulerna heter macos-user-isolation, icloud-storage-layer, etc. (INTE booking/seo)
- [ ] Varje modul har ≥3 steg i Användarflöde som är konkreta (inte "Research: determine...")
- [ ] macos-user-isolation har steg som "Create separate home directory /Users/openclaw" (från sub_components)
- [ ] Ingen modul har REST API-designsteg (från api-design.md)
- [ ] PROJECT.md nämner INTE "booking" eller "nextjs" eller CSS-färger

**Test 2: Booking (webbprojekt utan preflight)**
```
python -m engines.bridge --description "Booking site for fishing trips in Zanzibar with payment" \
  --feeling "professional" --color "blue" --location "zanzibar" --out .tmp/verify-web
```
Verifiera:
- [ ] Modulerna är booking-specifika (booking-catalog, booking-calendar, payment)
- [ ] booking-calendar har 11 files_to_create och 14-stegs användarflöde
- [ ] PROJECT.md visar "Kategori: booking", "Stack: nextjs" (korrekt för webbprojekt)

Om test 1 och test 2 båda passerar: syftet är uppfyllt. Processen fungerar för alla projekttyper.

---

## Vad du INTE ska göra

- Inte lägga till nya vault items (det kommer som resultat av enrichment, inte före)
- Inte ändra preflight-pipelinen (preflight fungerar — enrichment är gapet)
- Inte ändra forge_engine.py CATEGORY_MODULES (de är rätt för webbprojekt utan preflight)
- Inte ändra testsviten (lägg till nya tester, ta inte bort befintliga)
- Inte refaktorera bridge.py (ändra bara enrich_modules + _apply_preflight_to_workspace)

---

## Filer du behöver läsa innan du kodar

1. `engines/bridge.py` — sök `enrich_modules` och `_apply_preflight_to_workspace`
2. `v2/.buildr/preflight/openclaw-macbook-platform/PREFLIGHT_ARCHITECTURE.json` — se `sub_components` per komponent
3. `v2/.buildr/preflight/openclaw-macbook-platform/PREFLIGHT_ACCEPTANCE.json` — se `pass_condition` per kriterium
4. `vault/skills/component-enrichment.md` — den vault skill som beskriver processen (uppdatera om nödvändigt)

---

## Filmapp efter implementering

```
engines/bridge.py                              ← Ändring A, B, C
vault/skills/component-enrichment.md           ← Eventuell uppdatering
tests/test_end_to_end.py                       ← Nya verifieringstester
```

Inget annat ska ändras.
