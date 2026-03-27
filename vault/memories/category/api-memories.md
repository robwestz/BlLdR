# Memory: API Projects

## Scars (mistakes to never repeat)

### Scar: Unvalidated POST endpoint
**When:** Building the public contact form endpoint
**What happened:** Shipped a POST handler with no input validation — assumed only the form would call it
**Consequence:** A bot found the endpoint within 10 days and submitted 10,000 records with empty strings. Wrote a cleanup script that ran for 3 hours. Emergency validation patch deployed at midnight.
**Now we:** Every POST validates input at the handler boundary before touching the DB. Schema validation runs first, always.

### Scar: `SELECT *` leaking sensitive fields
**When:** Building the user profile API response
**What happened:** Returned the full Prisma row from the user endpoint without an explicit select
**Consequence:** The `password_hash` field appeared in the JSON response for 4 days before a developer caught it during a frontend integration. Security incident logged.
**Now we:** Never return a raw DB row. Define an explicit response DTO for every endpoint. Strip sensitive fields before the response leaves the handler.

### Scar: Inconsistent error response format
**When:** Building endpoints across 3 different sprints with different developers
**What happened:** Each endpoint returned errors in its own shape — some `{ error: string }`, some `{ message, code }`, some HTTP status with no body
**Consequence:** The frontend had 6 separate error-handling cases. Fixing the inconsistency required touching 40 files across 3 modules.
**Now we:** Define one error shape at project start. Use a shared error factory. All 30+ endpoints return identical error structures.

### Scar: No rate limiting on auth endpoints
**When:** After launch, during normal operation
**What happened:** Auth endpoints had no rate limiting — login and password reset were open
**Consequence:** One IP sent 2,000 login attempts per minute. Discovered only when a user filed a support ticket about "slow login." Emergency middleware patched that afternoon.
**Now we:** Rate limiting goes on auth endpoints before the first deploy. Not after.

## Insights (approaches to replicate)

### Insight: Define response types before implementing handlers
**When:** Building a new payments integration API from scratch
**What worked:** Wrote TypeScript response interfaces and a Postman collection contract before writing a single handler
**Why:** 3 schema mismatches caught at contract review that would have caused silent production bugs.
**Apply:** Write the response type and example payload first. Build the handler to match the contract.

### Insight: Shared error factory function
**When:** Standardizing error responses across a 30-endpoint API after the inconsistency incident
**What worked:** Created one `createApiError(code, message, details?)` factory imported everywhere
**Why:** All endpoints returned identical error shapes without any coordination overhead. Frontend wrote one error handler.
**Apply:** Create the error factory in the first file of any API project. Import it before writing the first handler.
