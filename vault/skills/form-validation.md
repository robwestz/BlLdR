# Skill: Form Validation

## When to Use
Building any form that accepts user input.

## Steps
1. Add `required` attribute to mandatory fields
2. Add `type` attribute matching data (email, url, number, tel)
3. Implement onBlur validation: validate the field when user leaves it
4. Show error message directly below the field, in red, immediately on blur
5. Implement onSubmit validation: re-validate ALL fields before submission
6. Prevent submission if any field fails validation
7. After failed submit, focus the first invalid field
8. On successful submit, disable the submit button to prevent double-submit
9. Show success feedback (message, redirect, or confirmation)

## Verification
- [ ] Required fields reject empty submission
- [ ] Email fields reject invalid format on blur
- [ ] Error messages appear below the specific field, not as alert()
- [ ] Submit button disables during submission
- [ ] First invalid field receives focus after failed submit
- [ ] Success state is visually distinct from error state

## Common Mistakes
- Alert boxes for validation: Use inline error messages instead
- Validating only on submit: Validate on blur AND submit
- Generic "form invalid" message: Tell the user WHICH field and WHY
- Allowing double-submit: Disable button + show loading state during submit
