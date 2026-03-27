# Constraint: No Implicit Any

## Scope
Always. All TypeScript files (.ts, .tsx).

## Prohibited Patterns

### ❌ Untyped variable declarations
**Banned:** `let data: any` or `let result` whose inferred type becomes `any`
**Why:** `any` propagates silently; typed code downstream loses all type safety without a single compiler warning.
**Instead:** Declare an explicit type or interface. If the shape is unknown: `let data: unknown` forces a type-guard before use.

### ❌ Untyped as-any casts
**Banned:** `(response as any).field` or `return value as any` without an explanatory comment
**Why:** The cast suppresses errors at the cast site but allows incorrect types to flow into callers, causing runtime failures far from the origin.
**Instead:** Add a comment stating why, then narrow: `// External API — schema not typed yet\n(response as ExternalApiResponse).field`.

### ❌ Function return type inferred as any
**Banned:** `function transform(input) { return input.data }` where return type infers as `any`
**Why:** Every consumer of the function inherits `any`, spreading unsafety across the entire call graph.
**Instead:** Annotate explicitly: `function transform(input: RawPayload): ProcessedData { ... }`.
