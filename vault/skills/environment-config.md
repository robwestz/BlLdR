# Skill: Environment Config

## When to Use
Setting up, accessing, or auditing environment variables and secrets across development, staging, and production.

## Steps
1. Create `.env.example` listing every required variable with placeholder values and a comment explaining each one
2. Add `.env`, `.env.local`, `.env.*.local` to `.gitignore` before the first commit
3. Create a single `config.ts` (or `env.py`, `config.go`, etc.) that reads and validates all env vars at startup — fail fast if any required var is absent
4. Separate per-environment files: `.env.development`, `.env.staging`, `.env.production`
5. Never call `process.env.VAR` (or language equivalent) directly in business logic — always import from the config module
6. Document each variable's purpose and expected format as a comment in `.env.example`

## Verification
- [ ] App exits with a clear error message when a required env var is missing at startup
- [ ] No `.env` file (with real values) appears in version control history
- [ ] `grep -r "process.env" src/` (or equivalent) returns zero results outside the config module
- [ ] `.env.example` contains every variable the app reads

## Common Mistakes
- Committing `.env` files: add to `.gitignore` before the very first commit, not after → rotate any secrets that were exposed
- Hardcoding fallback secrets (`|| 'dev-secret'`): silently runs insecure config in production → throw an error instead
- Reading env vars in every file that needs them: creates dozens of touch points per variable rename → centralise in one config module
- Putting secrets in `.env.example`: that file is committed → use placeholder strings like `YOUR_API_KEY_HERE`
