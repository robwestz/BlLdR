# Skill: Tailscale Mesh Setup

## When to Apply
Connecting two or more devices (Mac, Windows, Linux, VPS) via secure zero-config mesh networking.

## Steps

1. Install Tailscale on the host: `brew install tailscale` (macOS) or equivalent for the platform
2. Start and authenticate: `sudo tailscale up` — opens browser for login
3. Verify connection: `tailscale status` — shows the device in the tailnet
4. Install on the second device and repeat authentication with the same Tailscale account
5. Verify mesh: `tailscale ping <other-device-name>` — must succeed
6. For service exposure (e.g., gateway dashboard): `tailscale serve --bg <port>` — exposes to tailnet only
7. Verify serve: from the other device, open `https://<device-name>.<tailnet>.ts.net/` — must load

## Common Mistakes
- Using `tailscale funnel` instead of `tailscale serve` — funnel exposes to the PUBLIC internet, serve is tailnet-only.
- Running both the Mac App Store Tailscale and the Homebrew CLI — they conflict. Pick one.
- Forgetting to authenticate on both devices with the same account — they won't see each other.
- Not using `--bg` flag with serve — the serve command blocks the terminal without it.

## Verification
- `tailscale status` shows both devices as connected
- `tailscale ping <other-device>` returns latency (not timeout)
- Service URL accessible from the other device (if serve is configured)
- `tailscale whois <ip>` resolves to the expected device identity
