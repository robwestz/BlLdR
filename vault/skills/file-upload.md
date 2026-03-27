# Skill: File Upload

## When to Use
Accepting any file from a user — images, documents, or other binary data — and storing it safely.

## Steps
1. Validate file type server-side by reading the file signature (magic bytes), not the file extension or `Content-Type` header
2. Enforce a server-side file size limit before processing the payload (default: 10 MB for images, 50 MB for documents)
3. Generate a new unique filename server-side (UUID + original extension) — never use the client-provided filename as a storage key
4. Show a progress indicator for any upload that may take more than 1 second (files > ~1 MB)
5. Store files outside the web root or in object storage (S3, Cloudflare R2, etc.) — never in a publicly accessible server directory
6. Return a CDN URL or time-limited signed URL to the client — never expose the raw internal storage path
7. Schedule a cleanup job to delete failed, orphaned, or expired uploads

## Verification
- [ ] Uploading a file renamed from `.exe` to `.jpg` is rejected by the server-side magic-byte check
- [ ] A file exceeding the size limit is rejected with a clear error message before full processing begins
- [ ] The original client-provided filename is not used anywhere in the storage key or path
- [ ] A progress indicator is visible during uploads of files larger than 1 MB

## Common Mistakes
- Extension-only validation: renaming `malware.exe` to `photo.jpg` bypasses it entirely → check magic bytes server-side
- Storing uploads in the web root: allows direct HTTP access and potential execution of uploaded files → use object storage or a non-public directory
- Blocking the UI during upload: degrades UX and gives no feedback → use async upload with a progress bar
- Using sequential or predictable filenames: enables enumeration of other users' files → always generate a UUID-based name server-side
