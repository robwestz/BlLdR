# Memory: TypeScript

## Scars (mistakes to never repeat)

### Scar: `any` that metastasized
**When:** During rapid prototyping of a third-party integration
**What happened:** Used `any` on an API response to move fast, left a TODO comment
**Consequence:** `any` propagated into 15 downstream functions over 3 weeks. A field rename caused zero TypeScript errors but silent runtime failures in production — 6 hours of debugging across 4 files.
**Now we:** Ban `any` at lint level. Use `unknown` and narrow explicitly.

### Scar: Untyped API response fields
**When:** During the user profile feature
**What happened:** Fetched the profile endpoint and accessed `user.profile.avatar` without typing the response shape
**Consequence:** The API silently renamed the field to `avatarUrl` in a backend deploy. Production showed broken images for 2 days before anyone noticed.
**Now we:** Type every external API response at the fetch boundary before accessing any field.

### Scar: Interface used for a discriminated union
**When:** Building the notification system event model
**What happened:** Defined all event variants as interfaces extended from a base interface
**Consequence:** Spent 2 hours fighting TypeScript trying to narrow types in a switch statement — interfaces cannot model discriminated unions. Rewrote everything as type aliases.
**Now we:** Use `type` for unions and discriminated union patterns. `interface` only for object shapes meant to be extended.

### Scar: Enums bloating the bundle
**When:** Adding status enums across 8 API models
**What happened:** Used regular TypeScript enums throughout — they compile to runtime objects
**Consequence:** Bundle size increased by 4KB. Client flagged it during a Lighthouse audit. Had to migrate all enums in a cleanup sprint.
**Now we:** Use `const enum` or string literal union types. Never plain enums.

## Insights (approaches to replicate)

### Insight: Type at the fetch boundary
**When:** Building the payments integration
**What worked:** Wrote the full response type before touching a single response field, validated with a Zod schema on the way in
**Why:** Saved 3 separate debugging sessions where API field names differed from assumptions.
**Apply:** Define the response type and parse it at the network boundary. Never access fields on an untyped response.

### Insight: `satisfies` for config objects
**When:** Setting up environment config and feature flag objects
**What worked:** Used `satisfies` instead of explicit type annotation on config literals
**Why:** TypeScript validated the shape but still inferred the narrow literal types — best of both, zero casting needed.
**Apply:** Use `satisfies` on config objects, route maps, and constant lookup tables where you want validation without widening.
