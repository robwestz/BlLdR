# Constraint: Security Basics

## Scope
Always. All code handling user input, auth, or external data.

## Prohibited Patterns

### ❌ User input in HTML without sanitization
**Banned:** Rendering user-provided strings directly with innerHTML or dangerouslySetInnerHTML
**Why:** XSS — attacker injects script that steals sessions or exfiltrates data.
**Instead:** Use textContent or React's default JSX escaping. Use DOMPurify if HTML is required.

### ❌ Secrets in source code or git
**Banned:** API keys, database URLs, or passwords in frontend code, committed .env files, or comments
**Why:** Anyone can read client-side source. Bots scrape GitHub for exposed keys within minutes.
**Instead:** Server-side environment variables. Never commit .env. Rotate any key that was exposed.

### ❌ SQL/NoSQL injection
**Banned:** Concatenating user input into database queries: `"SELECT * WHERE id=" + userId`
**Why:** Attacker can read, modify, or delete the entire database with a crafted input.
**Instead:** Parameterized queries or ORMs. Never string concatenation with user-controlled values.

### ❌ Missing authorization on resource access
**Banned:** Checking authentication (is the user logged in?) without checking authorization (can THIS user access THIS resource?)
**Why:** IDOR — user A can access user B's data by changing an ID in the URL or request body.
**Instead:** For every resource fetch or mutation: verify the authenticated user owns or has permission to access that specific record.

### ❌ Auth bypass via missing middleware
**Banned:** Adding new routes or endpoints without explicitly applying authentication middleware
**Why:** New routes default to public unless protected. One missed route exposes the entire resource.
**Instead:** Deny by default. Opt-in to public routes, not opt-in to protected ones.
