# Buildr v2 — Gemini Session (Differentiated)

Du startar en ny session utan tidigare kontext.
Du är **Gemini** — din unika styrka är ditt **massiva kontextfönster**.

---

## Kontext

Claude har redan producerat v2-filerna. improve.md har genomförts.
Systemet har nu ~210 filer. Filer relaterade till v2 finns på flera ställen:

```
v2/                                          ← Source-of-truth (11 filer)
├── prompts/buildr-advanced-operator.md
├── skills/buildr-workspace-architect/SKILL.md + 6 references
├── claude.md                                ← Specen Claude jobbade från
├── start.md                                 ← Claudes bootstrap
└── improve.md                               ← Härdnings-backlog (genomförd)

skills/buildr-workspace-architect/           ← Installerad kopia (runtime path)
engines/preflight_validate.py                ← Python validator (binary gate)
skills/buildr-operator/references/preflight-ingest.md  ← Operator-integration
docs/v2-overview.md                          ← Flöde, paths, install
docs/workspace-from-preflight.md             ← Ingest-karta: preflight → workspace
docs/preflight-retention-policy.md           ← Git, retention, immutabilitet
vault/routines/preflight-gate-check.md       ← Ny rutin
vault/strategies/preflight-reopen.md         ← Ny strategi
requirements.txt                             ← jsonschema dependency
```

---

## Varför du och inte Claude eller Codex

Claude producerade v2-filerna.
Codex verifierar genom kodexekvering.
**Du** läser hela systemet simultant och hittar vad de missar.

---

## Ditt uppdrag

Producera tre audit-dokument. Läs ALLT — inte urval.

### Dokument 1: `v2/gemini-audit/CONSISTENCY_AUDIT.md`

Läs ALLA dessa (hela filer, inte skumning):

```
Tier 1 — Systemdefinition:
  BUILDR_ARCHITECTURE.md, MANIFEST.md, vault/INDEX.md, INIT.md, README.md

Tier 2 — Alla 6 system skills (SKILL.md + varje references/):
  skills/buildr-operator/ (inkl references/preflight-ingest.md)
  skills/buildr-executor/
  skills/buildr-smith/
  skills/buildr-scout/
  skills/buildr-rescue/
  skills/buildr-workspace-architect/ (installerad kopia — jämför med v2/skills/)

Tier 3 — v2-lagret:
  v2/prompts/buildr-advanced-operator.md
  v2/skills/buildr-workspace-architect/SKILL.md + alla 6 references
  v2/improve.md
  docs/v2-overview.md
  docs/workspace-from-preflight.md
  docs/preflight-retention-policy.md

Tier 4 — Engines:
  engines/forge_engine.py (hela)
  engines/bridge.py (hela)
  engines/vault_selector.py (hela)
  engines/imperfektum_engine.py (hela)
  engines/preflight_validate.py (hela)

Tier 5 — Templates:
  templates/CLAUDE.md, templates/RUN.md, templates/AGENT.md
  templates/EVALUATOR.md, templates/qa/gates.md
  templates/state/orchestration.yaml

Tier 6 — Vault (ALLA filer):
  vault/skills/ (33), vault/constraints/ (16), vault/strategies/ (13)
  vault/routines/ (14), vault/memories/ (20), vault/agents/ (4)

Tier 7 — Governance:
  docs/skill-governance.md
```

Sök efter:
- **Siffror som inte stämmer** mellan MANIFEST, INDEX, ARCHITECTURE, README
- **v2/skills/ vs skills/ drift** — har den installerade kopian divergerat från source?
- **Löften utan implementation** — refererar filer som inte finns
- **Motstridiga instruktioner** — INIT.md vs templates/CLAUDE.md vs skills
- **Dead code i engines** — funktioner som aldrig anropas
- **Trigger-överlapp** — workspace-architect vs operator vs scout
- **Schema-drift** — preflight-handoff.schema.json vs vad SKILL.md beskriver
- **Governance-violations** — vault items som inte uppfyller docs/skill-governance.md
- **Duplicering** — samma information på flera ställen med olika versioner

Format per finding:
```
FINDING: [Vad]
FILES: [Vilka filer]
EVIDENCE: [Exakt vad fil A säger vs fil B]
SEVERITY: BLOCKER | MAJOR | MINOR
RECOMMENDATION: [Vilken version som är korrekt]
```

**Krav: minst 10 findings. Om du hittar färre har du inte letat ordentligt.**

### Dokument 2: `v2/gemini-audit/CROSS_PATTERN_ANALYSIS.md`

Med hela systemet laddat:
- **Mönster som aldrig formaliserats** — upprepade patterns i vault skills utan egen rutin
- **Vault-luckor synliga i kontext** — saker engines gör som ingen vault skill beskriver
- **Governance-granskning av ALLA 33 vault skills** — uppfyller var och en standarden?
- **Skill-överlapp** — 6 system skills, krockar triggers eller scope?
- **Imperfektum-kvalitet** — matchar engine-output vault/memories/ mönstren?
- **v2 preflight vs befintliga quality gates** — överlapp med templates/qa/gates.md?

### Dokument 3: `v2/gemini-audit/V2_INTEGRATION_ASSESSMENT.md`

Givet att v2 nu existerar med alla filer:
- Vilka befintliga filer **har uppdaterats** men möjligen **inkonsekvent**?
- Var i forge_engine.py och bridge.py behöver v2-handoff integreras (exakta radnummer)?
- Överlappar preflight-gate-check.md med templates/qa/gates.md Gate 1?
- Är preflight-reopen.md konsekvent med approval.md?
- Matchar preflight_validate.py schemat i preflight-handoff.schema.json?
- Vilka rader i INIT.md bör referera v2 men gör det inte?

---

## Regler

- Du producerar INTE v2-filer (det har Claude gjort)
- Du producerar INTE kod (det gör Codex)
- Du producerar **audit-dokument** som kräver simultant laddat kontext
- Varje finding har exakt filreferens med radnummer där möjligt
- Governance-granskning täcker ALLA 33 vault skills, inte ett urval

---

## Output

```
v2/gemini-audit/
├── CONSISTENCY_AUDIT.md
├── CROSS_PATTERN_ANALYSIS.md
└── V2_INTEGRATION_ASSESSMENT.md
```
