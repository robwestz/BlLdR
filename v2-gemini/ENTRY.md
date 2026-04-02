# Buildr v2 — start här

**Denna fil är den enda du behöver peka på** (`@v2/ENTRY.md` i Cursor eller öppna den manuellt). Här listas vad som går att göra och var du går vidare — eller kör `.\v2\run.ps1` i repo-roten för en interaktiv meny i PowerShell.

---

## Snabböversikt — vad kan jag göra?

| # | Vill du … | Gå till / gör så här |
|---|-----------|----------------------|
| **1** | Förstå syfte, lager och agentavsikt | [`docs/BUILDR-purpose-and-layers.md`](../docs/BUILDR-purpose-and-layers.md) (spegel: [`v2/docs/purpose-and-layers.md`](docs/purpose-and-layers.md)) |
| **2** | Se hela v2-översikten (tabeller, länkar) | [`docs/v2-overview.md`](../docs/v2-overview.md) |
| **3** | Starta en session som *skriver/uppdaterar* v2-filer enligt spec | [`v2/start.md`](start.md) (följ `AUTHOR_GATE` i [`v2/claude.md`](claude.md)) |
| **4** | Köra *improve*-backlog och risker i ground-repo | [`v2/improve.md`](improve.md) |
| **5** | Köra **advanced operator** (preflight-prompt) | [`v2/prompts/buildr-advanced-operator.md`](prompts/buildr-advanced-operator.md) — kopiera in som system-/projektprompt där din agent stödjer det |
| **6** | Installera **workspace-architect**-skillen bredvid övriga skills | `cp -r v2/skills/buildr-workspace-architect/ skills/buildr-workspace-architect/` (PowerShell: se menyscript nedan) |
| **7** | **Validera** en preflight-staging-mapp (artefakter + JSON-schema) | `python -m engines.preflight_validate <staging-dir>` (repo rot) |
| **8** | Köra **tester** för validatorn / hela suite | `pytest tests/test_preflight_validate.py` eller `pytest` (repo rot) |
| **9** | Läsa canonical **schema**-placering | [`schemas/preflight/README.md`](../schemas/preflight/README.md) |

**Legacy vs advanced:** befintlig operator/workspace utan preflight = som tidigare. Advanced = preflight-faserna + godkännande innan generering; se [`skills/buildr-operator/SKILL.md`](../skills/buildr-operator/SKILL.md) (två ingångsvägar).

---

## För agenter (kort)

1. Läs denna fil om användaren pekar på v2 utan annan kontext.
2. Fråga inte "vad vill du?" i tomma — erbjud val från tabellen ovan eller kör `run.ps1` om användaren är i terminal.
3. För *endast* redigering av v2-artefakter enligt spec: följ [`v2/start.md`](start.md).

---

## Interaktiv meny (Windows)

Från **repo-roten**:

```powershell
.\v2\run.ps1
```

Menyn kör inget farligt utan bekräftelse där det behövs och visar exakta kommandon för validering och tester.

---

## Index över viktiga filer i `v2/`

| Sökväg | Roll |
|--------|------|
| `v2/ENTRY.md` | **Denna fil** — nav och val |
| `v2/run.ps1` | Interaktiv meny (PowerShell) |
| `v2/start.md` | Bootstrap för att författa v2 |
| `v2/claude.md` | Spec för v2-lagret |
| `v2/improve.md` | Backlog efter v2-hardening |
| `v2/prompts/buildr-advanced-operator.md` | Advanced operator-prompt |
| `v2/skills/buildr-workspace-architect/` | Preflight-skill + references + schema JSON |

---

*Senast tillagd som enda ingångspunkt för v2-arbetsflöden.*
