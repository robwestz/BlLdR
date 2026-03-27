# Constraint: No Synchronous Blocking Operations Inside Async Functions

## Scope
Always. All JavaScript/TypeScript files containing async functions or request handlers.

## Prohibited Patterns

### ❌ Synchronous file reads in async context
**Banned:** `fs.readFileSync(...)` or `JSON.parse(fs.readFileSync(...))` inside an `async` function
**Why:** Blocks the Node.js event loop for the entire read duration; all concurrent requests queue behind this operation.
**Instead:** Use `await fs.promises.readFile(...)` and `JSON.parse(await fs.promises.readFile(..., 'utf8'))`.

### ❌ Synchronous child process execution in async code
**Banned:** `child_process.execSync(cmd)` inside an async function or request handler
**Why:** Freezes the event loop for the full duration of the subprocess; under load this cascades into timeouts across all users.
**Instead:** Use `await execAsync(cmd)` via `util.promisify(child_process.exec)` or the `execa` library.

### ❌ Synchronous crypto or compression in hot paths
**Banned:** `crypto.pbkdf2Sync(...)` or `zlib.deflateSync(...)` inside an async route handler
**Why:** CPU-bound sync calls block the event loop; a single slow request stalls every other in-flight request.
**Instead:** Use the async variants with `await`: `await pbkdf2Async(...)` via `util.promisify`.
