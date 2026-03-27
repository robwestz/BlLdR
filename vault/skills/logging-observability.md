# Skill: Logging and Observability

## When to Use
Adding logging to any service, API, or background job that will run in production.

## Steps
1. Use a structured logger — output JSON objects, not string concatenation (`logger.info({ userId, action })` not `console.log("User " + id + " did thing")`)
2. Define log levels and use them consistently: `debug` (dev only), `info` (normal operations), `warn` (recoverable unexpected states), `error` (failures requiring attention)
3. Log at boundaries: requests in, responses out, external API calls, background job starts and ends
4. Include correlation IDs: every request gets a unique ID that propagates through all log lines for that request
5. Never log sensitive data: passwords, tokens, PII, payment card numbers — log the fact that an operation happened, not its payload
6. For errors: log the full stack trace, the input that caused the error (sanitized), and the user/session context
7. Set log level via environment variable — production defaults to `warn`, development to `debug`
8. Add at least one health check endpoint that confirms the service is alive and its dependencies are reachable

## Verification
- [ ] Log output is structured JSON, not free-form strings
- [ ] A request ID appears on every log line for a given request
- [ ] No passwords, tokens, or PII appear in any log output
- [ ] Error logs include stack trace and relevant context
- [ ] Log level is controlled by environment variable, not code changes
- [ ] Health check endpoint returns 200 when service is operational

## Common Mistakes
- Logging strings instead of objects: makes log aggregation and search impossible → always log structured key-value pairs
- Logging sensitive fields: GDPR violation and security risk → log IDs and event names, never payloads containing credentials
- No correlation ID: impossible to trace a request across multiple services → assign at entry point, pass through all calls
- Logging only on errors: when production fails, you need context that happened before the error → log key success paths too
