# Skill: launchd Daemon Setup

## When to Apply
Running a process as a persistent background service on macOS that starts on boot and restarts on crash.

## Steps

1. Create a plist file in `~/Library/LaunchAgents/` (user-level) or `/Library/LaunchDaemons/` (system-level):
   File name format: `com.<org>.<service>.plist`
2. Required plist keys:
   - `Label`: unique identifier (matches filename without .plist)
   - `ProgramArguments`: array of command + args (e.g., `["/usr/local/bin/node", "/path/to/app.js"]`)
   - `KeepAlive`: `true` (restart on crash)
   - `RunAtLoad`: `true` (start on boot/login)
   - `StandardOutPath` + `StandardErrorPath`: log file paths
3. Load the service: `launchctl load ~/Library/LaunchAgents/com.<org>.<service>.plist`
4. Verify running: `launchctl list | grep <service>`
5. Test crash recovery: `kill <pid>` — service should restart within seconds
6. Check logs: `tail -f <StandardOutPath>`

## Common Mistakes
- Putting user services in /Library/LaunchDaemons/ — they run as root, not as your user.
- Using `start` without `load` — service isn't registered yet.
- Setting KeepAlive without StandardErrorPath — crash reasons invisible.
- Hardcoding paths with `~` in plist — launchd doesn't expand tilde. Use full path: `/Users/<username>/...`

## Verification
- `launchctl list | grep <label>` shows PID (not `-` which means not running)
- `kill <pid>` followed by 5-second wait → `launchctl list` shows new PID (auto-restart worked)
- Log files exist and contain recent output
