#!/usr/bin/env python3
"""Run Claude skills for all projects."""

from skills import get_projects, run_project


def main():
    for project in get_projects():
        run_project(project)


if __name__ == "__main__":
    main()
