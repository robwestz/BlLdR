# Skill: Component Enrichment

## When to Apply
After preflight approval, before workspace generation. For each architectural component that will become a module.

## Steps

1. Read the component's name, description, and justification from preflight architecture.
2. Search vault: run `vault_selector.select_skills(component_description)` for matching skills.
3. If vault match found: read the vault skill. Extract concrete implementation steps from it.
4. If no vault match: research the component.
   - Search docs for the technology/platform involved.
   - Search web for "how to set up [component] on [platform]".
   - Read any referenced repos or config files.
5. Produce for each component:
   - `implementation_steps`: numbered list of concrete commands/actions in order.
   - `files_to_create`: exact file paths that will be created or configured.
   - `verification_commands`: commands that prove the step worked (exit 0 = pass).
   - `vault_items_used`: which vault items informed this component's steps.
6. Write results to PREFLIGHT_ENRICHMENT.json in the preflight staging directory.
7. If this component's pattern is reusable: flag for new vault item creation via buildr-smith.

## Common Mistakes
- Writing vague steps ("set up the database") instead of concrete commands (`brew install postgresql@16 && createdb openclaw`).
- Skipping verification — every step needs a way to confirm it worked.
- Not checking vault first — reinventing steps that already exist as vault skills.
- Enriching with information that isn't verified — always test commands or cite docs.

## Verification
- Every component has at least 3 implementation_steps.
- Every step is a concrete action (command, UI action, file creation), not a description.
- Every component has at least 1 verification_command.
