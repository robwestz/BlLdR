# Constraint: No Empty or Silent Catch Blocks

## Scope
Always. All languages. All try/catch, .catch(), rescue, except blocks.

## Prohibited Patterns

### ❌ Empty catch block
**Banned:** `catch (e) {}` or `except: pass` — a catch block with no body or only a comment
**Why:** The error is swallowed. The caller receives no signal. The bug is invisible until data is corrupted or a user reports it.
**Instead:** At minimum: log the error with its message and stack, then either re-throw or return a typed error response.

### ❌ Catching and ignoring the error variable
**Banned:** `catch { return null }` or `except Exception: return None` — error is not logged or re-thrown
**Why:** Callers receive null/None with no explanation. Debugging requires guessing which operation failed.
**Instead:** `catch (e) { logger.error(e); return null; }` — always log before swallowing.

### ❌ Catch-all in production logic
**Banned:** `catch (e: unknown) { return defaultValue }` without logging in a non-fallback context
**Why:** Masks any error — including ones that should stop execution — as a normal fallback state.
**Instead:** Catch specific error types. Use catch-all only at the top-level boundary, and always log there.
