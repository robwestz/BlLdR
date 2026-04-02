# Skill: iCloud Workspace Sync

## When to Apply
Using iCloud Drive as cloud-synced storage for a workspace or configuration directory on macOS.

## Steps

1. Ensure iCloud Drive is enabled: System Settings > Apple ID > iCloud > iCloud Drive (toggle on)
2. Identify the iCloud Drive local path: `~/Library/Mobile Documents/com~apple~CloudDocs/`
3. Create the workspace directory in iCloud: `mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/<workspace-name>`
4. Create a convenience symlink: `ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/<workspace-name> ~/<workspace-name>`
5. Verify sync: create a test file in the directory, wait 2-5 minutes, verify it appears on icloud.com or another device
6. For config sync: symlink config directory to iCloud location (e.g., `ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/<app>-config ~/.config/<app>`)

## Common Mistakes
- Symlinking IN the wrong direction — the real files must live in iCloud Drive, the symlink points TO them from the convenient location.
- Storing large binary files (>100MB) — iCloud sync slows dramatically. Keep workspace lean (text, config, small files).
- Relying on instant sync — iCloud has 1-5 minute delay. This is a feature (rollback window) but not real-time.
- Not enabling "Optimize Mac Storage" — without it, ALL iCloud files stay local, defeating the disk-saving purpose.
- Using symlinks inside iCloud Drive pointing OUT — iCloud does not follow symlinks; only files physically inside the iCloud directory sync.

## Verification
- `ls -la ~/Library/Mobile\ Documents/com~apple~CloudDocs/<workspace-name>/` shows files
- `brctl status` (or check iCloud Drive status in Finder sidebar) shows sync active
- Test file appears on icloud.com within 5 minutes
- `du -sh ~/Library/Mobile\ Documents/com~apple~CloudDocs/<workspace-name>/` shows reasonable size
