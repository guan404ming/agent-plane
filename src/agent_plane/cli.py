"""CLI entry point."""

import argparse
import sys

from agent_plane.runner import get_projects, run_project


def main():
    parser = argparse.ArgumentParser(description="Run Agent Plane skills")
    parser.add_argument("-p", "--project", help="Run specific project by name")
    parser.add_argument("-l", "--list", action="store_true", help="List available projects")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without running commands")
    args = parser.parse_args()

    projects = get_projects()

    if args.list:
        print("Available projects:")
        for p in projects:
            status = "enabled" if p.enabled else "disabled"
            print(f"- {p.name} ({status}) [{p.provider}] {p.schedule.cron}")
        return

    if args.project:
        projects = [p for p in projects if p.name == args.project]
        if not projects:
            print(f"Project '{args.project}' not found.")
            sys.exit(1)

    for project in projects:
        run_project(project, dry_run=args.dry_run)
