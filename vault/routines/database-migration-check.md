# Routine: Database Migration Check

## When to Run
Before running any database migration against a production or staging environment.

## Checklist
- [ ] Migration file is version-numbered and follows the project's naming convention
- [ ] Migration has been tested against a local copy of production data (not just the dev fixture)
- [ ] A rollback procedure exists and has been written down: either a `down()` migration or manual SQL
- [ ] Migration is non-destructive by default: columns are added before old ones are dropped; data is copied before source is removed
- [ ] If the migration locks a table, the expected lock duration is estimated and acceptable for current traffic
- [ ] Backup of the target database confirmed recent (within last 24 hours for production)
- [ ] Migration has been reviewed by at least one other person if it affects more than 1 table

## If Any Check Fails
Fix the specific failing check. Re-run this entire checklist. Do not run the migration until all pass.

## Duration
10-15 minutes.
