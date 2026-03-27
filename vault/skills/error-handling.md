# Skill: Error Handling

## When to Use
Any code that can fail: API calls, form submissions, file operations, parsing.

## Steps
1. Wrap the operation in try/catch (or .catch for promises)
2. In the catch block, determine error type (network, validation, auth, unknown)
3. Display a user-friendly error message (never show raw error objects)
4. Log the technical error for debugging (but not console.log in production)
5. Provide a recovery action: retry button, go-back link, or contact info
6. For loading states: show a spinner or skeleton BEFORE the operation
7. For empty states: show a helpful message with a suggested action
8. Never let the UI crash — wrap route-level components in error boundaries

## Verification
- [ ] Network failures show "connection error" message, not blank screen
- [ ] Invalid input shows specific field-level error
- [ ] Loading state visible during async operations
- [ ] Empty state has message AND action suggestion
- [ ] No raw error objects visible to the user

## Common Mistakes
- Swallowing errors silently: Always show something to the user
- "Something went wrong": Tell the user what to DO about it
- No loading state: Users need feedback that something is happening
