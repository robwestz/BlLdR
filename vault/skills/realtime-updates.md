# Skill: Realtime Updates

## When to Use
Delivering data changes from server to client without requiring a full page reload.

## Steps
1. Choose the mechanism based on traffic pattern: **Polling** for infrequent changes (> 1 min interval); **SSE** for one-directional server→client streams; **WebSocket** only when bidirectional communication is required
2. For polling: start with a 10–30 second interval and reduce only after measuring actual need
3. For SSE: set `Content-Type: text/event-stream` and `Cache-Control: no-cache`; the browser reconnects automatically on disconnect
4. For WebSocket: authenticate during the connection handshake — not on the first message after the socket is open
5. Implement exponential backoff on reconnection attempts: start at 1 s, double each attempt, cap at 30 s
6. Clean up connections (close socket / cancel interval / abort SSE) when the component or process shuts down

## Verification
- [ ] Connection is fully closed when the component unmounts or process exits (verified in DevTools Network tab)
- [ ] Disconnecting the network and reconnecting triggers automatic reconnection with backoff
- [ ] Authentication is checked before the connection is accepted, not after the first data frame
- [ ] Polling interval is ≥ 10 seconds unless a lower interval was validated by measurement

## Common Mistakes
- WebSocket for read-only data: SSE is simpler, works through HTTP proxies, and auto-reconnects → use SSE for server-push-only flows
- Polling at < 1 second intervals: burns server CPU and network for marginal latency gain → switch to SSE or WebSocket at that point
- No cleanup on unmount: leaves ghost connections open, accumulates memory leaks → always register a teardown handler
- Authenticating after the socket is open: allows a window where unauthenticated frames can arrive → authenticate during the upgrade handshake
