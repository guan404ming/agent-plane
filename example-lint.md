---
name: example-lint
description: Run Python linting with ruff and fix any issues.
---

# Python Lint

Run ruff linter and fix code style issues.

## Commands

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```
