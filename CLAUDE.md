# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                         # Install dependencies
uv run agent-plane --setup      # Install skills via openskills
uv run agent-plane --list       # List jobs
uv run agent-plane -p <name>    # Run specific job
uv run agent-plane --dry-run    # Simulate execution
uv run ruff check               # Lint
uv run ruff format              # Format
make start                      # Start scheduler daemon
make stop                       # Stop scheduler
```

## Architecture

Agent Plane automates AI agent workflows by scheduling and running skills against target repositories.

**Core flow:**

1. `get_jobs()` reads `jobs.json` for job configurations
2. Config is validated via Pydantic models (`Config`, `JobConfig`, `ScheduleConfig`)
3. `run_job()` invokes provider CLI with `/<skill>` command in target path (skills installed via openskills)
4. Scheduler uses APScheduler with cron triggers to run jobs on schedule

**Key modules:**

- `runner.py` - Job loading and execution (`get_jobs`, `run_job`, `setup`)
- `models.py` - Pydantic config validation with `extra="forbid"`
- `scheduler.py` - APScheduler daemon with `run_job_n_times` wrapper
- `cli.py` - CLI entry point via argparse

**Configuration:**

- `jobs.json` - Job definitions with skill references, target paths, providers, and schedules
- Skills are installed globally via `openskills` from the configured `skills_repo`

**Providers:** Configured in `PROVIDERS` dict in `runner.py`. Currently supports `claude` and `gemini` CLI tools.
