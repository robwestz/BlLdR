# Constraint: Security Basics

## Scope
Always. All code handling user input, auth, or external data.

### ❌ User input in HTML without sanitization
**Banned:** Rendering user-provided strings directly with innerHTML or dangerouslySetInnerHTML
**Why:** Cross-site scripting (XSS). Attacker injects script that steals sessions.
**Instead:** Use textContent or React's default JSX escaping. Sanitize if HTML is required.

### ❌ Secrets in client-side code
**Banned:** API keys, database URLs, or passwords in frontend code or git
**Why:** Anyone can read client-side source. Bots scrape GitHub for exposed keys.
**Instead:** Server-side environment variables. Never in .env files committed to git.

### ❌ SQL/NoSQL injection
**Banned:** Concatenating user input into database queries
**Why:** Attacker can read/delete/modify entire database.
**Instead:** Parameterized queries. ORMs. Never string concatenation for queries.
