# Skill: Input Sanitization

## When to Use
Before storing, processing, or rendering any data that originated from a user or external system.

## Steps
1. Validate type and format server-side before storing or acting on any input — client-side checks are UX only
2. Trim whitespace from all string inputs before validation
3. Sanitize HTML content with a whitelist-based library (DOMPurify or equivalent) — never write manual regex sanitizers
4. Validate file uploads by checking file signature (magic bytes) server-side, not file extension; re-encode images to strip embedded metadata
5. Use parameterized queries or ORM-managed queries for all database operations — never concatenate user input into SQL strings
6. Escape HTML entities (`<`, `>`, `&`, `"`, `'`) when rendering user-provided text into an HTML context

## Verification
- [ ] Submitting `<script>alert(1)</script>` as a text field renders as literal text, not an executed script
- [ ] SQL special characters in inputs do not alter query behavior or return unexpected rows
- [ ] A file renamed from `.exe` to `.jpg` is rejected by server-side MIME/magic-byte check
- [ ] All string inputs have leading and trailing whitespace removed before validation

## Common Mistakes
- Client-side-only validation: users bypass browser checks trivially → always re-validate every field server-side
- Manual HTML sanitization with regex: regex cannot reliably parse HTML and will miss edge cases → use a vetted library
- Trusting the `Content-Type` header for file uploads: header is set by the client and trivially spoofed → inspect the actual file bytes
- Sanitizing on output only: storing unsanitized data leaves it dangerous in logs, exports, and future rendering paths → sanitize at input time
