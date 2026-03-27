# Tools

> This file is generated per workspace and describes the tools available
> to the agent executing this project. Content depends on the deployment
> context (Claude Code, Codex, Gemini CLI, etc.).

## Available Tool Categories

### File Operations
- Read files
- Write files
- Create directories

### Shell / Terminal
- Run commands
- Execute scripts
- Check exit codes

### Browser / UI Testing
- Navigate to URLs *(if available in this deployment)*
- Take screenshots *(if available in this deployment)*
- Interact with page elements *(if available in this deployment)*

### Code Execution
- Run test suites
- Execute build commands
- Validate output

---

## Usage Notes

- Use file operations for all reads and writes — do not guess file contents
- Use shell for build, test, and lint commands — verify exit codes
- Use browser tools for UI verification when available — do not skip visual checks for UI projects
- If a tool category is not available, note it explicitly and find an alternative

---

*This file is populated by the Buildr operator when generating the workspace.
If it is empty or generic, update it to reflect the actual tools available.*
