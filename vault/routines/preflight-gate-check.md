# Routine: Preflight Gate Check

## When to Run
Before starting workspace generation in the advanced flow. Every time. No exceptions.

## Checks (binary — each passes or fails)

1. `PREFLIGHT_APPROVAL.json` exists in staging directory.
2. `status` field equals `approved`.
3. `approval_basis` is a non-empty array.
4. `allowed_next_step` equals `workspace_generation`.
5. All six `gates_verified` entries are `true`.
6. All 15 required preflight artifacts exist in the staging directory.

## If Fails
- Identify which check failed.
- Report the specific failure.
- Block workspace generation. Do not override.
- If status is `insufficient_information`: present `required_missing_inputs` to user.
- If status is `rejected`: present `rejection_reasons` to user.

## Expected Duration
Under 10 seconds (file existence checks + JSON field reads).

## Automation
Run `python engines/preflight_validate.py <staging-dir>` for the same checks with exit code 0/1.
