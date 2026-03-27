# Constraint: No Untyped Props

## Scope
Always. All React component files (.tsx).

## Prohibited Patterns

### ❌ Props typed as any
**Banned:** `function Button(props: any)` or `const Card = (props) => {}`
**Why:** Prop changes cause silent runtime failures with no TypeScript errors to catch them.
**Instead:** Define an explicit interface (`interface ButtonProps { label: string; onClick: () => void }`) and apply it.

### ❌ React.FC without generic
**Banned:** `const Card: React.FC = ({ title }) => {}`
**Why:** Props are implicitly typed as `{}`, so missing or misnamed props produce no compile-time error.
**Instead:** `const Card: React.FC<CardProps> = ({ title }) => {}` with a named interface above.

### ❌ Omitting destructuring to avoid declaring types
**Banned:** Receiving `props` as a whole object and accessing `props.x` without a typed interface
**Why:** Hides missing-prop errors; refactors break silently and are only caught at runtime.
**Instead:** Destructure typed props: `({ title, href }: LinkProps)` at the function signature.
