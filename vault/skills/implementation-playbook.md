# Skill: Implementation Playbook

## When to Apply
Starting implementation of a module that has a prescriptive spec (files, data model, components, user flow).

## Steps

1. Read the full module spec. Do not skim.
2. Read the contract for this module (contracts/[module-id].md).
3. Read SYSTEM.md §Design and §Kodstandard.
4. Re-read MEMORY.md section for this module.
5. Create files in the order listed in "Filer att skapa" — dependencies first.
6. For each data entity: define the TypeScript type/interface or Python model FIRST.
7. For each component: implement with exact props listed in spec. Start with the skeleton (props, return null), then fill in.
8. For each API route: implement the handler matching the contract endpoint spec.
9. Wire components together following the user flow, step by step.
10. For each acceptance criterion: verify it passes. Mark [x] in the module spec.
11. Run the project (`npm run dev` / `python -m app`). Fix errors before reporting.
12. Hand off to evaluator.

## Common Mistakes
- Starting with the UI before data types exist → prop mismatches, runtime errors.
- Implementing components in isolation without wiring them → works alone, breaks together.
- Skipping the contract check → building interfaces that don't match adjacent modules.
- Implementing all files before testing any → cascading errors that are hard to isolate.

## Verification
- Every file listed in spec exists and is non-empty.
- Every acceptance criterion is verifiable (not "looks good" — run it, click it, call it).
- The project runs without errors after this module.
