# Preflight JSON Schema — canonical location

**Single source of truth:** `v2/skills/buildr-workspace-architect/references/preflight-handoff.schema.json`

Den här mappen innehåller **ingen duplicerad** schema-fil (undviker drift mellan kopia och skill). Istället:

- `engines/preflight_validate.py` läser schemat från sökvägen ovan.
- IDE och framtida Forge/Bridge kan peka på samma fil.

Om du behöver en **repo-root**-alias senare: lägg antingen en symlink här (plattformsberoende) eller ett CI-steg som verifierar hash-match mot `v2/skills/.../preflight-handoff.schema.json`.

Se även: `v2/improve.md` (riskrad om dubbel sanning).
