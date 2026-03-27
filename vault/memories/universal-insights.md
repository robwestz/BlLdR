# Memory: Universal Insights

## Insights (approaches to replicate)

### Insight: Design system first
**When:** Project setup
**What worked:** We built the complete design system (CSS variables, base components, layout) before touching any feature
**Why:** Every subsequent module just used existing components. No design decisions during feature work. Massive speed boost.
**Apply:** Build the design system completely in its module. Test with a dummy page. Then never touch it during the build.

### Insight: One module at a time
**When:** Development workflow
**What worked:** Built and QA'd one module at a time, never starting the next until current passed all checks
**Why:** Problems caught small. Each module was solid before the next built on top. Zero cascading failures.
**Apply:** Follow the RUNBOOK exactly. The order exists for a reason.

### Insight: Five base components cover 90%
**When:** Component architecture
**What worked:** Created Button, Card, Input, Select, Modal — covered 90% of UI needs
**Why:** Consistency was automatic. New features assembled from existing pieces. Site looked coherent.
**Apply:** Build those 5 in the design system. Use them everywhere. Custom only for truly unique UI.

### Insight: Responsive per module
**When:** Responsive design
**What worked:** Tested 320px, 768px, 1024px after EVERY module, not just at the end
**Why:** Responsive issues fixed in context while code was fresh. End-of-project fixes are 5x harder.
**Apply:** Every module QA includes responsive check at three breakpoints.

### Insight: Feeling as north star
**When:** Client satisfaction
**What worked:** The finished product matched the described feeling exactly
**Why:** Client felt understood. Trusted the output because it matched their mental image.
**Apply:** The feeling in SYSTEM.md is not a suggestion. It's the north star. Every decision filters through it.
