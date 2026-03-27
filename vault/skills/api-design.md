# Skill: API Endpoint Design

## When to Use
Creating any server endpoint or API route.

## Steps
1. Choose HTTP method: GET (read), POST (create), PUT (replace), PATCH (update), DELETE
2. Design URL path: `/api/[resource]/[id]` — noun-based, plural
3. Define request body type (for POST/PUT/PATCH)
4. Define response body type (always typed, never `any`)
5. Define error response format: `{ error: string, code: string }`
6. Validate input at the handler level before any business logic
7. Return appropriate status codes: 200, 201, 400, 401, 404, 500
8. Handle the error case BEFORE the success case in the handler code

## Verification
- [ ] URL follows `/api/resource/id` pattern
- [ ] Request and response types are defined
- [ ] Input validation runs before business logic
- [ ] Error responses have consistent format
- [ ] Correct HTTP status codes used

## Common Mistakes
- Verb-based URLs (/api/getUsers): Use noun-based (/api/users)
- Missing input validation: Always validate before processing
- Returning 200 for errors: Use appropriate status codes
