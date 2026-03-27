# Skill: Data Modeling

## When to Use
Defining data structures for any entity in the system.

## Steps
1. Identify the entity and its purpose in one sentence
2. List all fields with name, type, and whether required or optional
3. Add `id: string` (always required, always unique)
4. Add `createdAt: string` and `updatedAt: string` (ISO 8601)
5. Identify relationships: which other entities does this reference?
6. Use references (IDs) not nested objects for relationships
7. Define an enum for any field with a fixed set of values
8. Add validation constraints in comments (min/max, format, allowed values)
9. Export the type from a shared types file

## Verification
- [ ] Entity has id, createdAt, updatedAt
- [ ] All fields have explicit types (no `any`)
- [ ] Relationships use ID references, not nested objects
- [ ] Enums used for fixed-value fields
- [ ] Type is exported from shared types file

## Common Mistakes
- Nesting related objects: Use ID references for relationships
- Missing timestamps: Always include createdAt and updatedAt
- Using `any` type: Be explicit about every field's type
