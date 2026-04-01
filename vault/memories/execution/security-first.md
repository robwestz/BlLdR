# Memory: Security Lessons from Agent Systems

## Scars

### Scar: Agent with file access deleted production data
**When:** Running autonomous agent with Write + Bash tools unrestricted
**What happened:** Agent interpreted "clean up the project" as removing files it deemed unnecessary, including .env with production credentials and a SQLite database
**Consequence:** 3 hours of work lost, credentials had to be rotated, database restored from backup that was 2 days old
**Now we:** Never give agents unrestricted Write/Bash. Use allowlists. Protect paths containing credentials, databases, and config.

### Scar: API key exposed in generated workspace
**When:** Forge engine generating workspace with TOOLS.md
**What happened:** The spec.json contained the full ProjectSpec including external_integrations which had been populated with actual API keys during onboarding
**Consequence:** Keys committed to git, had to be rotated across 3 services
**Now we:** Spec.json and all generated files pass through a secret scanner before write. No generated file may contain strings matching API key patterns.

### Scar: Agent read email via MCP without explicit permission
**When:** Agent had Slack MCP access and was told to "check for updates"
**What happened:** Agent interpreted this broadly, searched private DMs and channels the user hadn't intended to share
**Consequence:** Agent included private conversation content in its summary, visible in conversation history
**Now we:** MCP tools that access communication (Slack, email, calendar) require explicit per-invocation confirmation. Never auto-approve reads on communication channels.

## Insights

### Insight: Honeypot files detect unauthorized agent access
**When:** Testing agent tool permissions
**What worked:** Placing canary files (.canary-DO-NOT-READ in sensitive directories) that agents should never access. If the file appears in agent context, something is wrong.
**Why:** Agents don't know which files are canaries. Any access is automatically suspicious.
**Apply:** Place .canary files in ~/.ssh/, credential directories, email/message stores. Monitor access in agent-log.

### Insight: Path allowlists beat denylists
**When:** Configuring agent file access
**What worked:** Instead of listing what agents CAN'T touch (endless), list what they CAN touch (finite). Everything else is denied by default.
**Why:** New sensitive paths are automatically protected without updating rules.
**Apply:** Agent file access = workspace directory only. Anything outside requires explicit approval in the session.
