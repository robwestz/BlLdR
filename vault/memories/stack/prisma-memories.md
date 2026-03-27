# Memory: Prisma

## Scars (mistakes to never repeat)

### Scar: Unbounded `findMany` in production
**When:** Building the admin order list endpoint
**What happened:** Called `prisma.findMany()` with no `take` or pagination; development DB had 20 records
**Consequence:** Production had 80,000 orders. The endpoint timed out under real load within 3 days of launch. DBA had to add an emergency index and we patched pagination at 11pm.
**Now we:** Every `findMany` has `take` and cursor-based pagination. No exceptions, even for "internal" endpoints.

### Scar: Four-level deep `include`
**When:** Building the user profile card component's data layer
**What happened:** Used nested `include` four levels deep: user → posts → comments → likes → author
**Consequence:** The query took 8 seconds and returned 2MB of JSON to render a single card. Prisma loaded the full social graph. Fixed by rewriting to two targeted queries.
**Now we:** Treat any `include` deeper than 2 levels as a red flag. Flatten with targeted queries or `select`.

### Scar: Related writes without a transaction
**When:** Implementing the checkout flow
**What happened:** Created a payment record, then updated order status in a second separate Prisma call
**Consequence:** The second call failed during a DB hiccup. Inventory marked items as sold, order status stayed "pending". Took 40 minutes to reconcile 12 affected records manually.
**Now we:** Any write that touches more than one table goes inside `$transaction`. Always.

### Scar: Migration run in production without a backup
**When:** Renaming a column in the users table
**What happened:** Ran `prisma migrate deploy` directly in production; the migration had a typo in the column rename
**Consequence:** Column data was inaccessible. Rollback was manual SQL and took 40 minutes. The app was in maintenance mode for 35 of those minutes.
**Now we:** Snapshot the DB before every migration. Run migrations through CI with a verified rollback script.

## Insights (approaches to replicate)

### Insight: `select` instead of `include` for list views
**When:** Optimizing the customer list endpoint
**What worked:** Switched from `include: { profile: true }` to `select` with only the 5 displayed fields
**Why:** The query dropped from 340ms to 28ms on the same dataset because Prisma stopped loading 20 unused columns.
**Apply:** List queries always use `select`. Only fetch the fields that render. `include` is for detail views.

### Insight: `$transaction` for all multi-step writes
**When:** Refactoring the order fulfillment service after the checkout incident
**What worked:** Wrapped every multi-table write in `prisma.$transaction([...])` with explicit rollback
**Why:** Zero partial-state bugs in 6 months after adoption across 14 write endpoints.
**Apply:** Open `$transaction` first. Write the operations inside. Close. Never write to two tables outside a transaction.
