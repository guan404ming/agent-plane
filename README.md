# 🤖 Agent Plane

[![Python 3.12](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: Apache](https://img.shields.io/badge/License-apache-yellow.svg)](https://opensource.org/license/apache-2-0)

Define, Schedule and Run.

## Quick Start

```bash
# 0. Install dependencies
uv sync

# 1. Create a skill
mkdir -p skills/my-project
echo '{"name":"my-project","path":"/path/to/repo","enabled":true,"provider":"claude"}' > skills/my-project/config.json
echo 'Fix all TODO comments in the codebase' > skills/my-project/prompt.jinja

# 2. Run once
make run

# 3. Or schedule it
make start
```

## Usage

```bash
make start   # Start scheduler
make stop    # Stop scheduler
make status  # Check status
make logs    # View logs
make run     # Run once
```

## Skills Folder Structure

```
skills/
├── _common.jinja        # Shared prompt blocks
└── <project>/
    ├── config.json
    ├── prompt.jinja
    ├── SKILL.md
    └── *.md
```

## Config

`skills/<project>/config.json`:

```json
{
  "name": "project-name",
  "path": "/path/to/repo",
  "enabled": true,
  "provider": "claude",
  "schedule": {
    "cron": "0 14 * * *",
    "times": 1
  }
}
```

| Field            | Description                  |
| ---------------- | ---------------------------- |
| `name`           | Project identifier           |
| `path`           | Path to target repository    |
| `enabled`        | Enable/disable project       |
| `provider`       | `claude` or `gemini`         |
| `schedule.cron`  | Cron expression (local time) |
| `schedule.times` | Runs per trigger             |

## License

Apache 2.0
