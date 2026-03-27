# Skill: Database Schema

## When to Use
Designing or modifying a relational database schema, from initial creation to iterative migrations.

## Steps
1. Name tables as plural nouns in snake_case: `user_profiles`, `order_items` — not `UserProfile` or `orderItem`
2. Name columns in snake_case: `created_at`, `first_name` — not `createdAt` or `FirstName`
3. Add `created_at` and `updated_at` timestamp columns to every table
4. Use UUIDs or ULIDs for primary keys on user-facing tables — never expose sequential integers that reveal record counts
5. Declare foreign key constraints at the database level — never rely on application logic alone to maintain referential integrity
6. Write every schema change as a numbered migration file; never modify the database structure directly
7. Add an index on every foreign key column and every column that appears in a WHERE or ORDER BY clause

## Verification
- [ ] Every table has `created_at` and `updated_at` columns
- [ ] All foreign key relationships are enforced by database-level constraints
- [ ] Every schema change exists as a versioned, sequential migration file
- [ ] No schema change was applied to any environment directly without a migration

## Common Mistakes
- Editing production schema directly: bypasses review and version history → always use a migration file
- Defaulting all columns to nullable: forces null checks everywhere → explicitly decide NOT NULL vs nullable for each column
- Missing indexes on foreign key columns: every JOIN becomes a full table scan → index every FK column at creation time
- Sequential integer PKs on public resources: reveals record count and enables enumeration → use UUID or ULID
