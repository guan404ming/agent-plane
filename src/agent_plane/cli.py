"""CLI entry point."""

import argparse
import sys

from agent_plane.runner import get_jobs, run_job, setup


def main():
    parser = argparse.ArgumentParser(description="Run Agent Plane skills")
    parser.add_argument("-p", "--project", help="Run specific job by name")
    parser.add_argument("-l", "--list", action="store_true", help="List available jobs")
    parser.add_argument(
        "--setup", action="store_true", help="Install skills via openskills"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without running commands",
    )
    args = parser.parse_args()

    if args.setup:
        setup()
        return

    jobs = get_jobs()

    if args.list:
        print("Available jobs:")
        for j in jobs:
            status = "enabled" if j.enabled else "disabled"
            print(f"- {j.name} /{j.skill} ({status}) {j.schedule.cron}")
        return

    if args.project:
        jobs = [j for j in jobs if j.name == args.project]
        if not jobs:
            print(f"Job '{args.project}' not found.")
            sys.exit(1)

    for job in jobs:
        run_job(job, dry_run=args.dry_run)
