# Onboarding

Ask these questions in conversation. Adapt based on what the user
already revealed. Skip questions whose answers are obvious from context.
Never ask more than 8 questions total.

## Questions

1. **Vision** — "Beskriv med en eller två meningar vad du vill bygga."
2. **Audience** — "Vem är det här till för?"
3. **Brand** — "Finns det redan färger, logotyp eller en stil du vill använda?"
4. **Feeling** — "Hur vill du att det ska kännas? (professionellt, lekfullt, lyxigt, enkelt)"
5. **Scope** — [Category-specific: what features, what flows, what content]
6. **Context** — "Var i världen ska det här användas?" (derive language, device, integrations)

## Answer Schema

Save to `state/orchestration.yaml` under `onboarding:`:

```yaml
onboarding:
  vision: ""
  audience: ""
  location: ""
  languages: []
  feeling: ""
  color_hint: ""
  scope:
    must_have: []
    nice_to_have: []
    non_goals: []
  category: ""
  owner_type: ""
onboarding_complete: true
```

## Derivation Rules

After saving answers, derive (do not ask):
- Tech stack (from category + features)
- Modules (from category + scope)
- Design system (from feeling + color + location)
- Integrations (from location + features)
- Device strategy (from audience + location)

Log all derivations in `state/orchestration.yaml` under `derivations:`.
