"""Skills module."""

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

SKILLS_DIR = Path(__file__).parent
LOGS_DIR = SKILLS_DIR.parent / "logs"

PROVIDERS = {
    "claude": [
        "claude",
        "-p",
        "{prompt}",
        "--dangerously-skip-permissions",
        "--model",
        "sonnet",
    ],
    "gemini": ["gemini", "-p", "{prompt}", "--model", "gemini-3-pro-preview", "--yolo"],
}


def get_projects() -> list[dict]:
    """Get all project configs."""
    projects = []
    for project_dir in SKILLS_DIR.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue
        config_file = project_dir / "config.json"
        if config_file.exists():
            config = json.loads(config_file.read_text())
            config["_dir"] = project_dir
            projects.append(config)
    return projects


def run_project(config: dict, dry_run: bool = False):
    """Run skills for a project."""
    if not config.get("enabled"):
        return

    project_dir = config["_dir"]
    target_path = Path(config["path"])
    provider = config.get("provider", "claude")

    if not target_path.exists():
        print(f"Path not found: {target_path}")
        return

    prompt = ""
    prompt_file = project_dir / "prompt.jinja"

    if prompt_file.exists():
        env = Environment(loader=FileSystemLoader(SKILLS_DIR))
        template = env.get_template(f"{project_dir.name}/prompt.jinja")
        prompt = template.render()

    skill_files = list(project_dir.glob("*.md"))
    cmd = [arg.replace("{prompt}", prompt) for arg in PROVIDERS[provider]]

    if dry_run:
        print(f"[DRY RUN] Would copy files to {target_path}:")
        for skill_file in skill_files:
            print(f"  - {skill_file.name}")
        print(f"[DRY RUN] Would run command in {target_path}:")
        print(f"  {' '.join(cmd)}")
        return

    copied = []

    try:
        for skill_file in skill_files:
            dest = target_path / skill_file.name
            shutil.copy(skill_file, dest)
            copied.append(dest)

        print(f"Running {provider} on {config['name']}")
        result = subprocess.run(
            cmd,
            cwd=target_path,
            capture_output=True,
            text=True,
        )

        # Save output
        LOGS_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOGS_DIR / f"{config['name']}_{provider}_{timestamp}.log"
        log_file.write_text(result.stdout + result.stderr)
        print(f"Output saved to {log_file}")

    finally:
        for f in copied:
            f.unlink(missing_ok=True)
