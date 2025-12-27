#!/usr/bin/env python3
"""List all configured projects."""

from skills import get_projects


def main():
    projects = get_projects()
    if not projects:
        print("No projects configured.")
        return

    max_name_len = max(len(p["name"]) for p in projects)
    max_provider_len = max(len(p.get("provider", "claude")) for p in projects)

    print(f"{'Project':<{max_name_len}}  {'Status':<8}  {'Provider':<{max_provider_len}}  Schedule")
    print("-" * (max_name_len + max_provider_len + 40))

    for project in sorted(projects, key=lambda p: p["name"]):
        name = project["name"]
        status = "enabled" if project.get("enabled") else "disabled"
        provider = project.get("provider", "claude")
        schedule = project.get("schedule", {})
        cron = schedule.get("cron", "-")
        times = schedule.get("times", 1)
        schedule_str = f"{cron} (x{times})" if times > 1 else cron

        print(f"{name:<{max_name_len}}  {status:<8}  {provider:<{max_provider_len}}  {schedule_str}")


if __name__ == "__main__":
    main()
