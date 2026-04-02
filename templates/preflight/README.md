# Preflight → workspace (mallar)

**Normativ ingest-karta:** `docs/workspace-from-preflight.md` (vilka `PREFLIGHT_*`-fält som styr vilka genererade filer).

Den här mappen är **inte** en andra sanning. `templates/preflight/INGEST.md` skapas inte förrän vi medvetet vill duplicera (undvik — länka till `docs/workspace-from-preflight.md`).

**Placeholders** (`<!-- BUILDR-PREFLIGHT:* -->`) i `templates/WORKSPACE.md` m.m. läggs **inte** in förrän `forge_engine.py` / generator faktiskt **injicerar** innehåll från preflight — annars blir det döda kommentarer (se `v2/improve.md`, riskrad om mallar).
