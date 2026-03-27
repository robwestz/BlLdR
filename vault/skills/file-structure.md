# Skill: Project File Organization

## When to Use
Setting up or reorganizing a project's file structure.

## Steps
1. Group by feature/module, not by file type (not all components in /components)
2. Shared code goes in /shared or /core (used by 3+ modules)
3. Each module gets its own directory with all its files
4. Maximum directory depth: 3 levels (src/modules/booking/components.tsx)
5. File names in kebab-case: `booking-calendar.tsx`, not `BookingCalendar.tsx`
6. One component per file (exception: small helper components)
7. Index files only for re-exports, never for logic
8. Config files at project root, never nested
9. Types shared across modules go in a central types file

## Verification
- [ ] No directory deeper than 3 levels
- [ ] Shared code is in /shared or /core, not duplicated
- [ ] File names are kebab-case
- [ ] No logic in index files
- [ ] Config files at root level

## Common Mistakes
- Grouping by type (/components, /hooks, /utils): Group by feature
- Deep nesting (src/modules/booking/views/calendar/components/): Max 3 levels
- Business logic in index.ts: Index files only re-export
