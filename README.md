# Agent Plane

Schedule and run AI agent skills against target repositories.

## Quick Start

```bash
uv sync
uv run agent-plane --setup      # Install skills via openskills
uv run agent-plane --list       # List jobs
uv run agent-plane -p tvm       # Run a job
uv run agent-plane --dry-run    # Simulate
make start                      # Start scheduler
make stop                       # Stop scheduler
```

## Config

`jobs.json` (or `jobs.local.json` for per-machine override):

```json
{
  "skills_repo": "guan404ming/claude-code-skills",
  "email": { "to": "you@gmail.com" },
  "jobs": [
    {
      "name": "tvm",
      "skill": "tvm-dev",
      "path": "../tvm",
      "enabled": true,
      "schedule": { "cron": "0 4 * * *", "times": 2 }
    }
  ]
}
```

SMTP credentials in `.env`:

```
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your_app_password
```

## License

Apache 2.0
