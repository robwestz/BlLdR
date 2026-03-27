# Memory: Python Projects

## Scars

### Scar: No virtual environment
**When:** Project setup
**What happened:** Installed packages globally, conflicted with another project
**Consequence:** Version mismatch broke the other project. 2 hours debugging.
**Now we:** Always create venv first. `python -m venv .venv && source .venv/bin/activate`. Always.

### Scar: No type hints
**When:** Six months into maintenance
**What happened:** Functions returned different types depending on input, no type annotations
**Consequence:** Every function call required reading the implementation to understand return types.
**Now we:** Type hints on every function signature. `def process(data: list[dict]) -> Result:`

## Insights

### Insight: Pathlib over os.path
**When:** File handling
**What worked:** Used pathlib.Path instead of os.path for all file operations
**Why:** Cleaner API, cross-platform, fewer string concatenation bugs.
**Apply:** `from pathlib import Path`. Never `os.path.join()`.
