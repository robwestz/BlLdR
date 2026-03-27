# Constraint: No Direct Database Access in UI Components

## Scope
Always. All files under `/components/`, `/app/` (client), or any file rendering JSX.

## Prohibited Patterns

### ❌ ORM import in component file
**Banned:** `import prisma from 'lib/db'` inside a React component or page client file
**Why:** Bundlers include the import in the client bundle, exposing DB credentials to the browser.
**Instead:** Move all DB calls to a server action, API route, or service layer; import the result only.

### ❌ Raw SQL in component files
**Banned:** `const rows = await db.query('SELECT * FROM users')` inside a component
**Why:** Breaks the server/client boundary; query runs client-side or leaks schema to the network layer.
**Instead:** Place the query in a dedicated data-access file (`/lib/data/users.ts`) and call it from the server side only.

### ❌ ORM model calls in client files
**Banned:** `await User.findMany(...)` or `await db.user.findFirst(...)` in files marked `'use client'`
**Why:** Next.js/bundler cannot tree-shake server-only modules; causes hydration errors and credential leaks.
**Instead:** Fetch via a typed API endpoint or server action that returns only the data the component needs.
