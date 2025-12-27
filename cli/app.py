"""CLI entry point."""

import argparse
import sys
from skills import get_projects, run_project


def main():
    parser = argparse.ArgumentParser(description="Run Agent Plane skills")
    parser.add_argument("-p", "--project", help="Run specific project by name")
    parser.add_argument("-l", "--list", action="store_true", help="List available projects")
    args = parser.parse_args()

    projects = get_projects()

    if args.list:
        print("Available projects:")
        for p in projects:
            status = "enabled" if p.get("enabled") else "disabled"
            print(f"- {p['name']} ({status})")
        return

    if args.project:
        projects = [p for p in projects if p["name"] == args.project]
        if not projects:
            print(f"Project '{args.project}' not found.")
            sys.exit(1)

    for project in projects:
        run_project(project)
