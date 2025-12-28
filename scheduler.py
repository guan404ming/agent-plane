#!/usr/bin/env python3
"""Run Claude skills with APScheduler based on config schedules."""

import sys
from datetime import datetime, timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from models import ProjectConfig
from skills import get_projects, run_project

# Unbuffered output for logging
sys.stdout.reconfigure(line_buffering=True)


def run_project_n_times(config: ProjectConfig):
    """Run a project N times based on schedule.times config."""
    times = config.schedule.times
    name = config.name

    for i in range(times):
        print(f"[{datetime.now().astimezone()}] [{name}] Running {i + 1}/{times}")
        run_project(config)
        print(f"[{datetime.now().astimezone()}] [{name}] Completed {i + 1}/{times}")


def main():
    scheduler = BlockingScheduler()
    local_tz = datetime.now().astimezone().tzinfo

    print(f"Current local time: {datetime.now().astimezone()}")
    print(f"Timezone: {local_tz}")
    print("-" * 50)

    for project in get_projects():
        if not project.enabled:
            continue

        cron = project.schedule.cron
        trigger = CronTrigger.from_crontab(cron, timezone=local_tz)
        scheduler.add_job(
            run_project_n_times,
            trigger,
            args=[project],
            id=project.name,
            name=f"Run {project.name}",
            max_instances=1,
        )
        next_run = trigger.get_next_fire_time(None, datetime.now(timezone.utc))
        print(f"Scheduled: {project.name}")
        print(f"  Cron: '{cron}', Times: {project.schedule.times}")
        print(f"  Next run: {next_run}")

    if not scheduler.get_jobs():
        print("No scheduled jobs found. Exiting.")
        return

    scheduler.start()


if __name__ == "__main__":
    main()
