# Buildr v2 — Codex Session (Differentiated)

Du startar en ny session utan tidigare kontext.
Du är **Codex** — din unika styrka är att du kan **exekvera kod i en sandbox**.

---

## Kontext

Claude har producerat v2-filerna. improve.md har genomförts.
Nyckelartifakter som behöver verifieras genom exekvering:

```
engines/preflight_validate.py                ← Python validator att testa
v2/skills/.../preflight-handoff.schema.json  ← JSON Schema att validera
engines/forge_engine.py                      ← ScaffoldGenerator att köra
engines/bridge.py                            ← WorkspaceBuilder.from_blueprint() att testa
engines/vault_selector.py                    ← select_for_wave() att testa
memory-system/tools/project-registry.sh      ← Bash-verktyg att köra
memory-system/tools/vault-select.sh          ← Bash-wrapper att testa
requirements.txt                             ← Dependencies att installera
```

---

## Varför du och inte Claude eller Gemini

Claude producerade filerna.
Gemini auditerar hela systemet för inkonsekvenser.
**Du** kör koden, validerar schemat, testar pipelinen.

---

## Steg 0: Setup

```bash
cd /path/to/buildrhel
pip install -r requirements.txt  # jsonschema etc
```

---

## Ditt uppdrag

### Test 1: Validera JSON-schemat

```python
import json, jsonschema

schema_path = "v2/skills/buildr-workspace-architect/references/preflight-handoff.schema.json"
schema = json.load(open(schema_path))

# 1a. Är det en giltig JSON Schema?
jsonschema.Draft7Validator.check_schema(schema)
print("PASS: Schema is valid Draft 7")

# 1b. Skapa sample-payloads för varje fas baserat på schemat
# och validera mot schemat. Rapportera PASS/FAIL per payload.
```

Output: `v2/codex-tests/schema-validation-results.md`

### Test 2: Kör preflight_validate.py

```python
# engines/preflight_validate.py är den binära gaten.
# Skapa en minimal godkänd preflight-output i en tempkatalog
# och kör validatorn mot den.

# Testa:
# a) Komplett godkänd preflight → PASS
# b) Saknad PREFLIGHT_APPROVAL.json → FAIL
# c) status: rejected → FAIL
# d) Tomt approval_basis → FAIL
# e) high reversibility_cost utan user_explicit → FAIL
```

Output: `v2/codex-tests/validator-results.md`

### Test 3: Forge integration

```python
from engines.forge_engine import ScaffoldGenerator, ProjectSpec, ProjectBlueprint, ModuleSpec, ModulePriority, ProjectCategory, TechStack
import tempfile, os

# Skapa en minimal blueprint och generera workspace
spec = ProjectSpec(
    project_name="codex-test",
    category=ProjectCategory.WEB_APP,
    tech_stack=TechStack.NEXTJS,
    description="Test project for Codex validation",
)
modules = [ModuleSpec(id="foundation", order=1, name="Foundation", priority=ModulePriority.FOUNDATION, description="Test")]
blueprint = ProjectBlueprint(spec=spec, modules=modules)

with tempfile.TemporaryDirectory() as out:
    gen = ScaffoldGenerator()
    files = gen.generate(blueprint, out)
    
    # Verifiera:
    assert os.path.exists(os.path.join(out, "CLAUDE.md")), "CLAUDE.md missing"
    assert os.path.exists(os.path.join(out, "agents", "agent-manifest.json")), "Agent manifest missing"
    assert os.path.exists(os.path.join(out, "qa", "gates.md")), "Quality gates missing"
    assert os.path.exists(os.path.join(out, "MEMORY.md")), "MEMORY.md missing"
    # Kontrollera att MEMORY.md INTE är en placeholder
    memory = open(os.path.join(out, "MEMORY.md")).read()
    assert "scaffold placeholder" not in memory.lower(), "MEMORY.md is still placeholder"
    
    print(f"PASS: Generated {len(files)} files")
```

Output: `v2/codex-tests/forge-integration-results.md`

### Test 4: Bridge med Imperfektum

```python
from engines.bridge import WorkspaceBuilder

# Kör from_blueprint() — ska generera Imperfektum-minne, vault-selection, och scaffold
builder = WorkspaceBuilder()
with tempfile.TemporaryDirectory() as out:
    files = builder.from_blueprint(blueprint, out)
    
    # Verifiera att Bridge ger MER än bara Forge
    memory = open(os.path.join(out, "MEMORY.md")).read()
    assert "Imperfektum" in memory or "Mistakes We Made" in memory, "Imperfektum not generated"
    assert os.path.exists(os.path.join(out, "vault-selection")), "Vault selection missing"
    
    print(f"PASS: Bridge generated {len(files)} files (vs Forge alone)")
```

Output: `v2/codex-tests/bridge-results.md`

### Test 5: Vault selector

```python
from engines.vault_selector import select_for_wave, select_skills, select_constraints

# Testa grundfunktioner
skills = select_skills("booking calendar form validation")
assert len(skills) > 0, "No skills selected for booking calendar"
assert "form-validation" in [s.stem for s in skills], "form-validation not selected"

constraints = select_constraints("A")
assert len(constraints) > 0, "No constraints for tier A"

# Testa select_for_wave
result = select_for_wave(intent="auth login signup", tier="B", category="web-app", stack="nextjs")
assert "skills" in result
assert "constraints" in result
assert "routines" in result
assert "memories" in result

# Edge cases
empty = select_skills("")
assert isinstance(empty, list)  # Ska inte krascha

print(f"PASS: vault_selector works ({len(skills)} skills, {len(constraints)} constraints)")
```

Output: `v2/codex-tests/vault-selector-results.md`

### Test 6: Memory-system tools

```bash
# project-registry.sh
bash memory-system/tools/project-registry.sh --list

# vault-select.sh (om det fungerar på plattformen)
bash memory-system/tools/vault-select.sh --intent "api design" --tier B 2>&1 || echo "SKIP: vault-select requires Python path fix"

# doctor.sh
bash memory-system/tools/doctor.sh --verbose
```

Output: `v2/codex-tests/memory-tools-results.md`

### Test 7: Befintliga tester

```bash
python -m pytest tests/ -v
```

Output: `v2/codex-tests/existing-tests-results.md`

---

## Efter tester: grundrepo-backlog

När tester är gröna, använd `v2/improve.md` som canonical lista över vad
grundrepot bör få. Uppdatera inte en separat kopia — länka och implementera
mot `v2/improve.md` så inget divergerar.

---

## Regler

- Du producerar INTE v2-spec-filer (Claude har gjort det)
- Du producerar INTE audit-dokument (Gemini gör det)
- Du **exekverar, validerar, och rapporterar**
- Varje test har PASS/FAIL med exakt felmeddelande vid FAIL
- Installera dependencies om de saknas
- Om ett test kräver en fil som inte existerar ännu: skapa en minimal mock

---

## Output

```
v2/codex-tests/
├── schema-validation-results.md
├── validator-results.md
├── forge-integration-results.md
├── bridge-results.md
├── vault-selector-results.md
├── memory-tools-results.md
└── existing-tests-results.md
```

Avsluta med:
```
TOTAL: X/Y tests passed
BLOCKERS: [lista]
READY FOR INTEGRATION: YES/NO
```
