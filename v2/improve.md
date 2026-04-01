# Buildr v2 — grundrepo: starkare bas för workspace-sammansättning

Detta dokument är en **valfri men högvärd** backlog för **grundrepot** (allt utanför själva `v2/skills/buildr-workspace-architect/*` som Claude/v2-specen producerar). Målet: när preflight är klar och workspace ska sättas ihop ska output från `v2/.buildr/preflight/<slug>/` bli **styrd, validerbar och spårbar** input — inte bara bra markdown.

## När du kör detta

- **BTW:** Plocka en punkt när du ändå rör `engines/`, `docs/`, eller operator-mallar.
- **Efter v2 byggt klart:** Kör backlogen systematiskt när `AUTHOR_GATE: PASS` finns och filerna ligger under `v2/prompts/` + `v2/skills/buildr-workspace-architect/`.
- **I samma system:** `v2/start.md` pekar hit efter PASS; `v2/claude.md` kräver att författaren nämner denna fil i *Final implementation note* (se specen).

Inget här ersätter v2-preflight-skillen. Det här **kopplar grundrepot** till den.

---

## 1. Maskinellt kontrakt mot framtiden (Forge / Bridge)

| Förslag | Poäng |
|--------|--------|
| `schemas/preflight/preflight-handoff.schema.json` **eller** `contracts/preflight/preflight-handoff.schema.json` — **en** canonical kopia i grundrepo, med tydlig regel om den är samma som `v2/skills/.../references/preflight-handoff.schema.json` (kopia vs symlink vs “v2 references re-export”) | IDE, CI och senare Python kan validera mot **en** sanning — minskar drift mellan skill och motor. |
| `engines/preflight_validate.py` (eller tunn CLI) som läser `v2/.buildr/preflight/<slug>/PREFLIGHT_APPROVAL.json` + övriga fas-JSON mot schemat, exit code ≠ 0 vid fel | **v1.5:** binär grind utan full Forge-integration; agent eller CI kör före “generate workspace”. |

**Varför gamechanger:** Stänger gapet mellan “prompt säger godkänd” och **verifierbart** godkänd.

---

## 2. Sammansättningskartor (vad preflight *driver* i workspace)

| Förslag | Poäng |
|--------|--------|
| `docs/workspace-from-preflight.md` eller `templates/preflight/INGEST.md` | Tabell: vilket `PREFLIGHT_*`-fält → vilken genererad fil/sektion (t.ex. CRI → topp av `PROJECT.md`, acceptance → `qa/` eller `contracts/`, decisions → `state/orchestration.yaml`). |
| `catalog/preflight-bindings.json` (eller YAML) | Maskinläsbar: `purpose_claims` / kategori → vault skill-id, tier, modulhints — minskar att operator/vault-selector **improviserar bort** från preflight. |

**Varför gamechanger:** Preflight blir **styrd kompositionsmotor**, inte bilaga.

---

## 3. Operator- och malllager i grundrepo

| Förslag | Poäng |
|--------|--------|
| `skills/buildr-operator/references/preflight-ingest.md` (kort) | Om `PREFLIGHT_APPROVAL.json` finns: dessa fält är normativa; konflikt → samma conflict protocol som i v2 integration. |
| Uppdatera `templates/WORKSPACE.md` / `templates/PROJECT.md` med stabila placeholders, t.ex. `<!-- BUILDR-PREFLIGHT:CRI -->` | Gör injektion av CRI / acceptance / decisions **deterministisk** vid generering. |

**Varför gamechanger:** Varje genererat workspace blir **spårbart** mot preflight utan manuell omskrivning.

---

## 4. Styrdokument och upptäckbarhet

| Förslag | Poäng |
|--------|--------|
| `docs/v2-overview.md` (en sida: flöde, paths, install, v1 prompt-gate vs v2 kod-gate, länk `v2/start.md`, länk hit) | Nya sessioner hittar v2 och kör inte legacy-operator av vana. |
| Uppdatera `README.md`, `MANIFEST.md`, `BUILDR_ARCHITECTURE.md` (sektion Preflight / v2) | Repo-“sanningskällor” stämmer med runtime. |

**Varför gamechanger:** Minskar **två sanningar** mellan `skills/` och `v2/skills/`.

---

## 5. Vault (agnostiskt, återanvändbart)

| Förslag | Poäng |
|--------|--------|
| `vault/strategies/preflight-reopen.md` (inom radgräns i `docs/skill-governance.md`) | Binära regler: när får purpose/arkitektur ändras efter approval. |
| `vault/routines/preflight-gate-check.md` | Binär rutin: finns fil X, validerar schema, `status == approved` — körbar före “skapa workspace-mapp”. |

**Varför gamechanger:** Samma grind för **alla** projekttyper.

---

## 6. Git och reproducerbarhet

| Förslag | Poäng |
|--------|--------|
| `.gitignore` (eller dokumenterad policy) för `v2/.buildr/` | Undvik att staging committas av misstag — eller medveten “evidence commit”-policy. |
| `docs/preflight-retention-policy.md` | Overwrite vs versionerade kataloger, immutability efter approval — i linje med v2-specen. |

**Varför gamechanger:** Leverans till kund utan att **läcka** eller **tappa** beslutsunderlag.

---

## Prioritet (minsta paket med störst lyft)

1. Repo-root schema + valideringsscript (eller CI-steg).  
2. Ingest-/bindings-karta + ev. `preflight-bindings.json`.  
3. Operator reference + mall-placeholders.  
4. `docs/v2-overview.md` + README / MANIFEST / BUILDR_ARCHITECTURE.  
5. Vault strategy + routine för reopen + gate-check.

---

## Risker och fallgropar (läs innan agent kör improve — och efteråt)

Peka en agent på **denna fil** och be den **checka av punkterna** innan den ändrar kod; annars skapar improve ofta “gröna” ändringar som ändå ger trasig runtime eller drift.

| Risk | Vad som går fel | Minsta åtgärd |
|------|------------------|---------------|
| **`v2/.buildr/` saknas i root `.gitignore`** | Preflight-JSON/md med användartext, antaganden eller känsliga detaljer kan committas av misstag. | Lägg `v2/.buildr/` i repots **root** `.gitignore`. Om ni *medvetet* committar audit-filer: dokumentera **undantag** (negation) i samma fil + i `docs/preflight-retention-policy.md` så policy och git inte motsäger varandra. |
| **Skill inte installerad till `skills/`** | Runtime (Claude Code, Cursor, m.fl.) som bara skannar `skills/` hittar aldrig `buildr-workspace-architect`; advanced flow känns “sönder” trots bra filer under `v2/skills/`. | Efter ändringar: verifiera att `skills/buildr-workspace-architect/SKILL.md` finns (symlink eller kopia enligt `integration-with-operator.md`). På **Windows** misslyckas ofta `ln -s` utan rätt rättigheter — använd då **rekursiv kopia** och dokumentera i README att kopian måste uppdateras när `v2/skills/` ändras. |
| **`buildr-operator` utan tydlig preflight-ingång** | Agenter som bara läser operator-SKILL missar advanced path och `preflight-ingest.md`. | **Åtgärdat i repot:** `skills/buildr-operator/SKILL.md` har avsnittet **Two entry paths** (legacy vs advanced), länk till `references/preflight-ingest.md`, `docs/v2-overview.md`, `python -m engines.preflight_validate`, och `vault/routines/preflight-gate-check.md`. |
| **Dubbel sanning för JSON Schema** | Ni lägger `schemas/preflight/*.json` i root men uppdaterar bara den **eller** bara `v2/skills/.../preflight-handoff.schema.json` → CI säger PASS medan skillen och valideraren divergerar. | Välj **en** canonical fil; andra vägen = symlink, copy-steg i CI, eller ett skript “sync schema”. Agenten ska **inte** lägga till andra kopior utan sync-regel. |
| **`preflight_validate` utan beroenden** | Script som använder `jsonschema` kraschar med ImportError i ren miljö. | Lägg beroende i `requirements.txt` / `pyproject.toml` **eller** dokumentera `pip install jsonschema` och gör validering valfri i CI tills det är fixat. |
| **Mall-placeholders utan Forge-koppling** | Ni lägger `<!-- BUILDR-PREFLIGHT:* -->` i `templates/` men `forge_engine.py` / `bridge.py` skriver aldrig dit innehåll → genererade workspaces får döda kommentarer och ingen spårbarhet. | Antingen: koppla injektion i kod i **samma** PR som malländringen, eller: lägg **inte** in placeholders förrän ingest finns (annars falsk trygghet). |
| **`catalog/preflight-bindings.json` vs faktisk vault** | Bindings pekar på vault-namn som inte finns eller som byter namn → tyst fel vid urval. | Efter införande: kör en enkel **existenskontroll** (filer under `vault/skills/` etc.) mot alla id:n i bindings, eller generera bindings från ett script som läser vault. |
| **Dokumentation säger “v2 finns” men MANIFEST/README glöms** | Nya bidragsgivare använder legacy-operator och undrar varför preflight “saknas”. | Uppdatera `MANIFEST.md` + `README.md` + ev. `BUILDR_ARCHITECTURE.md` **i samma fönster** som du börjar marknadsföra v2 — inte veckor senare. |
| **Flera kopior av v2-spec (`v2-codex/`, `v2-gemini/`, …)** | Agent följer fel `claude.md` och producerar artefakter som inte stämmer med `v2/skills/` i produktion. | Canonical spec för **innehåll i repot** är `v2/claude.md`. Övriga mappar = verktygssessioner; ändra dem bara om du medvetet speglar master. |
| **Godkänd preflight + manuell röra i staging** | Någon redigerar filer under `v2/.buildr/preflight/<slug>/` efter `approved` → workspace och “sanning” divergerar. | Efter improve: påminn i `docs/preflight-retention-policy.md` att **immutability efter approval** gäller; ändringar = **reopen** ny körning / ny slug enligt v2-regler. |

**Snabb sanity-check efter improve-pass (agent ska rapportera PASS/FAIL per rad):**

1. Root `.gitignore` innehåller `v2/.buildr/` **eller** dokumenterad undantagspolicy är komplett.  
2. `skills/buildr-workspace-architect/SKILL.md` finns om du ska köra advanced flow i denna clone.  
3. Finns repo-root schema-kopia: den är synkad med `v2/skills/.../preflight-handoff.schema.json` **eller** endast en path används överallt.  
4. `MANIFEST.md` nämner `buildr-workspace-architect` (eller tydligt säger att v2 endast är staging — men då får det inte stå motsatsen i README).  
5. `skills/buildr-operator/SKILL.md` innehåller **Two entry paths** (se riskraden ovan).  
6. `python -m pytest tests/test_preflight_validate.py -v` passerar (regression på v1.5-grinden).  

---

## Koppling till v2-systemet (redan inbyggt)

| Mekanism | Roll |
|----------|------|
| `v2/improve.md` (denna fil) | Canonical backlog; **ändra här** när ni implementerar eller avstår. |
| `v2/start.md` | Efter `AUTHOR_GATE: PASS`: nästa steg kan vara att arbeta igenom denna backlog. |
| `v2/claude.md` | Författaren ska i **Final implementation note** nämna `v2/improve.md` och vad som **delegerats** till grundrepo (se bullets i specen). |

Om du duplicerar v2-träd (t.ex. `v2-codex/`): länka till **`v2/improve.md`** som master-backlog så innehållet inte divergerar.
