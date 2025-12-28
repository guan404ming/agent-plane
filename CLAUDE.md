# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                         # Install dependencies
uv run agent-plane --list       # List projects
uv run agent-plane -p <name>    # Run specific project
uv run agent-plane --dry-run    # Simulate execution
uv run ruff check               # Lint
uv run ruff format              # Format
make start                      # Start scheduler daemon
make stop                       # Stop scheduler
```

## Architecture

Agent Plane automates AI agent workflows by scheduling and running skills against target repositories.

**Core flow:**

1. `get_projects()` scans `skills/` for project directories with `config.json`
2. Config is validated via Pydantic models (`ProjectConfig`, `ScheduleConfig`)
3. `run_project()` copies `*.md` skill files to target repo, runs provider CLI, then cleans up
4. Scheduler uses APScheduler with cron triggers to run projects on schedule

**Key modules:**

- `runner.py` - Project discovery and execution (`get_projects`, `run_project`)
- `models.py` - Pydantic config validation with `extra="forbid"`
- `scheduler.py` - APScheduler daemon with `run_project_n_times` wrapper
- `cli.py` - CLI entry point via argparse

**Skills structure:**

- `skills/<project>/config.json` - Project configuration (validated by Pydantic)
- `skills/<project>/prompt.jinja` - Optional Jinja2 prompt template
- `skills/<project>/*.md` and `skills/<project>/SKILL.md` - Skill files temporarily copied to target repo during execution

**Providers:** Configured in `PROVIDERS` dict in `runner.py`. Currently supports `claude` and `gemini` CLI tools.
