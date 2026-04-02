# Skill: macOS User Isolation

## When to Apply
Setting up a dedicated macOS user account for service isolation (agent, daemon, automated system).

## Steps

1. Create a Standard (non-admin) user via System Settings > Users & Groups, or terminal:
   `sudo sysadminctl -addUser <username> -fullName "<Full Name>" -password "<password>"`
2. Verify the user is Standard: `dscl . -read /Users/<username> UserShell` — should be `/bin/zsh`
3. Verify no admin: log in as the new user, run `sudo -v` — must fail with auth error
4. Enable FileVault for the new user (System Settings > Privacy & Security > FileVault > Enable Users)
5. Sign into a separate Apple ID / iCloud account from the new user (System Settings > Apple ID)
6. Verify separate Keychain: `security list-keychains` from the new user shows its own keychain, not the main user's
7. Verify TCC isolation: the new user has no pre-granted Accessibility, Full Disk Access, or Camera permissions

## Common Mistakes
- Creating the user as Administrator — defeats isolation. Standard users cannot sudo.
- Sharing the same Apple ID — credentials, Keychain items, and iCloud data leak between users.
- Granting Full Disk Access to Terminal.app on the service user — gives the agent access to all user data on the machine.
- Forgetting FileVault — disk is readable by booting to recovery without FileVault.

## Verification
- `sudo -v` fails on the service user (no admin)
- `dscl . -read /Users/<username> AuthenticationAuthority` shows separate SecureToken
- Service user's Keychain is independent (test: add a key, verify it doesn't appear on main user)
