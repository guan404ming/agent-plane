"""Run skills with APScheduler based on config schedules."""

import sys
import traceback
from datetime import datetime

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_MISSED
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from agent_plane.models import ProjectConfig
from agent_plane.runner import get_projects, run_project

# Unbuffered output for logging
sys.stdout.reconfigure(line_buffering=True)


def run_project_n_times(config: ProjectConfig):
    """Run a project N times based on schedule.times config."""
    times = config.schedule.times
    name = config.name

    print(f"[{datetime.now().astimezone()}] [{name}] Job triggered")

    try:
        for i in range(times):
            print(f"[{datetime.now().astimezone()}] [{name}] Running {i + 1}/{times}")
            run_project(config)
            print(f"[{datetime.now().astimezone()}] [{name}] Completed {i + 1}/{times}")
        print(f"[{datetime.now().astimezone()}] [{name}] Job finished successfully")
    except Exception as e:
        print(f"[{datetime.now().astimezone()}] [{name}] Job failed: {e}")
        traceback.print_exc()


def job_executed_listener(event):
    """Log when a job executes successfully."""
    print(f"[{datetime.now().astimezone()}] APScheduler: Job '{event.job_id}' executed")


def job_error_listener(event):
    """Log when a job encounters an error."""
    print(
        f"[{datetime.now().astimezone()}] APScheduler: Job '{event.job_id}' raised exception: {event.exception}"
    )


def job_missed_listener(event):
    """Log when a job is missed."""
    print(
        f"[{datetime.now().astimezone()}] APScheduler: Job '{event.job_id}' missed its scheduled time"
    )


def main():
    scheduler = BlockingScheduler()
    local_tz = datetime.now().astimezone().tzinfo

    # Add event listeners for debugging
    scheduler.add_listener(job_executed_listener, EVENT_JOB_EXECUTED)
    scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)
    scheduler.add_listener(job_missed_listener, EVENT_JOB_MISSED)

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
        # Use local time for next_run calculation to match the trigger timezone
        next_run = trigger.get_next_fire_time(None, datetime.now(local_tz))
        print(f"Scheduled: {project.name}")
        print(f"  Cron: '{cron}', Times: {project.schedule.times}")
        print(f"  Next run: {next_run}")

    if not scheduler.get_jobs():
        print("No scheduled jobs found. Exiting.")
        return

    print("-" * 50)
    print(f"[{datetime.now().astimezone()}] Scheduler started. Waiting for jobs...")
    scheduler.start()


if __name__ == "__main__":
    main()
