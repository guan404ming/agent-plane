"""CLI entry point."""

import argparse
import sys
from pathlib import Path

from skills import get_projects, run_project


def main():
    parser = argparse.ArgumentParser(description="Run Agent Plane skills")
    parser.add_argument("-p", "--project", help="Run specific project by name")
    parser.add_argument("-l", "--list", action="store_true", help="List available projects")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without running commands")
    args = parser.parse_args()

    projects = get_projects()

    if args.list:
        print(f"{'Name':<15} {'Status':<10} {'Provider':<10} {'Path'}")
        print("-" * 80)
        for p in projects:
            status = "enabled" if p.get("enabled") else "disabled"
            path_str = p.get("path", "")
            path_exists = Path(path_str).exists() if path_str else False
            path_status = "" if path_exists else " (NOT FOUND)"
            print(f"{p['name']:<15} {status:<10} {p.get('provider', 'claude'):<10} {path_str}{path_status}")
        return

    if args.project:
        projects = [p for p in projects if p["name"] == args.project]
        if not projects:
            print(f"Project '{args.project}' not found.")
            sys.exit(1)

    for project in projects:
        run_project(project, dry_run=args.dry_run)