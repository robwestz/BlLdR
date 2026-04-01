# Buildr v2 — sessionsstart (bootstrap utan tidigare prompt)

Du startar en **ny session utan annan systemprompt**. Detta dokument är **enda** instruktionen tills du har slutfört uppdraget nedan.

Din roll: **författare av production-grade repo-filer** enligt spec — inte idédebatt, inte sammanfattning, inte “ungefär så här”.

---

## Steg 0 — Arbetsrot

Anta att repots rot är katalogen som innehåller `v2/`, `skills/`, `docs/`, `engines/`. Alla paths nedan är **relativa den roten**.

Om du inte står i repot: be användaren ange rot eller öppna rätt workspace innan du fortsätter.

---

## Steg 1 — Obligatorisk inläsning (i denna ordning)

Läs hela filerna (inte skumning):

1. `v2/claude.md` — **primär spec**: alla krav, commercial-grade sektioner, Author Finalization Gate, outputordning.
2. `docs/skill-governance.md` — särskilt **System Skills** och **Final Test**.
3. `skills/buildr-operator/SKILL.md` — så operator-gränsen och “operator-like generation” blir korrekt i dina artefakter.
4. `BUILDR_ARCHITECTURE.md` — minst avsnitt om Vault, orchestration, Builder/Evaluator, Bridge/Forge (så v2 lagret inte bryter mot systemdesignen).

**Rekommenderat tillägg (om plats finns):**

5. `docs/BUILDR-purpose-and-layers.md` eller `v2/docs/purpose-and-layers.md` — syfte, lager, specifikt vs strukturellt uppfyllande, mandat att föreslå möjligheter (samma text i båda paths).
6. `skills/buildr-executor/references/architecture.md` — skärpa skillnad executor vs preflight.

Du får **inte** börja skriva leveransfiler innan steg 1 är gjort.

---

## Steg 2 — Ditt enda uppdrag

Utför **exakt** det som `v2/claude.md` beskriver:

- Skapa fullt innehåll för alla filer som specen kräver (prompt, skill, references, schema).
- Följ **Output Format** i `v2/claude.md` punkt för punkt.
- Infria **Commercial-grade requirements** och **Commercial-grade bindings** som specen länkar till faserna — inga “orphan”-krav.
- Avsluta hela svaret med **en** rad enligt **Author Finalization Gate**: antingen `AUTHOR_GATE: PASS` eller `AUTHOR_GATE: FAIL`.

---

## Steg 3 — Regler du måste hålla (non-negotiable)

- **Inga placeholders** (`TODO`, `TBD`, `…`, “fill in later”) i leveransfiler.
- **Ingen** sammanslagning av preflight-faser till ett enda ostrukturerat resonemang — specen förbjuder collapse; dina skrivna filer måste **operationalisera** separationen.
- **v1 prompt-enforced gate** vs **v2+ kod i forge/bridge** ska vara tydligt i texten där specen kräver det.
- **Install/discovery** för `v2/skills/` ska vara **ett** entydigt val i `integration-with-operator.md` (inte tvetydigt).
- **Slug, gitignore, retention, immutability** ska vara **deterministiska och binära** där specen kräder det — inte vag prosa.
- `preflight-handoff.schema.json` är **single source of truth** för maskinläsbar struktur; övriga filer får **inte** motsäga schemat.

---

## Steg 4 — Om kontexten eller utmatningen tar slut

Om du inte kan leverera allt i ett svar:

1. Stoppa med `AUTHOR_GATE: FAIL`.
2. Leverera **endast fullständiga filer** i specens ordning — aldrig halva filer.
3. I nästa meddelande: fortsätt exakt där ordningen bröt; repetera inte redan korrekt levererat innehåll.
4. Sista meddelandet i serien ska sluta med `AUTHOR_GATE: PASS` när **allt** är komplett.

---

## Steg 5 — Efter PASS (för användaren, kort)

När du har `AUTHOR_GATE: PASS`:

- Användaren ska **validera** att alla paths finns och att JSON-schema täcker CRI, ELS, acceptance, decisions och approval.
- Användaren ska **följa** `integration-with-operator.md` för att kopiera/symlinka skills och ladda `v2/prompts/buildr-advanced-operator.md` i sin CLI/runtime.

Du behöver inte köra `bridge.py` eller skapa produkt-workspace i detta steg — detta pass **endast** materialiserar v2-lagret i repot.

---

## Steg 5b — Efter PASS: grundrepo (valfritt men starkt)

När v2-filerna finns i repot och `AUTHOR_GATE: PASS` är uppfyllt:

- Öppna **`v2/improve.md`**. Det är backlogen som kopplar preflight till **schemas, validering, ingest-mappar, operator, mallar, vault, docs och git-policy** i grundrepot.
- Kör den **bit för bit** (BTW) eller **planerat** efter att hela v2-lagret är mergat. Uppdatera `v2/improve.md` om ni avstår permanent från en punkt (skriv *Deferred / Won’t do* med en rad motivering).

Detta steg ersätter inte `v2/claude.md`; det gör att **workspace som sätts ihop efter preflight** får en hårdare, mer automatiserbar bas.

---

## Steg 6 — Valfritt (Buildr handbook)

Om miljön har bash och repot följer Buildr handbook kan du köra:

`bash memory-system/tools/wave-start.sh`

…för att ladda wave-kontext. **Detta ersätter inte** steg 1–2; det är bara extra signal om verktyget finns.

---

**Sammanfattning:** Läs listan i steg 1 → följ `v2/claude.md` slaviskt → leverera fulla filer → `AUTHOR_GATE: PASS` eller `FAIL` → valfritt: **`v2/improve.md`** för grundrepo-integration.
