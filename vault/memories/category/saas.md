# Memory: SaaS Projects

## Scars

### Scar: Billing before core product
**When:** Feature planning
**What happened:** Built billing integration before the core product was stable
**Consequence:** Core features changed twice. Had to rewire billing each time. Three weeks wasted.
**Now we:** Core product works fully before billing wraps around it.

### Scar: Premature multi-tenancy
**When:** Architecture phase
**What happened:** Built full tenant isolation before having a single working tenant
**Consequence:** Massive complexity for zero users. First tenant took 3x longer to onboard.
**Now we:** Single-tenant first. Prove the product. Add multi-tenancy when the second customer arrives.

## Insights

### Insight: Onboarding is the product
**When:** User acquisition
**What worked:** We invested 30% of the build budget in the onboarding flow
**Why:** Users who completed onboarding retained. Users who didn't, churned. Onboarding WAS the product.
**Apply:** Build onboarding as a first-class module, not an afterthought.
