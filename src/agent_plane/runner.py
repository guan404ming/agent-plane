"""Job runner - load config and execute skills via openskills."""

import json
import subprocess
from datetime import datetime
from pathlib import Path

from agent_plane.models import Config, JobConfig

ROOT_DIR = Path(__file__).parent.parent.parent
JOBS_FILE = ROOT_DIR / "jobs.json"
LOGS_DIR = ROOT_DIR / "logs"

PROVIDERS = {
    "claude": [
        "claude",
        "-p",
        "{prompt}",
        "--dangerously-skip-permissions",
        "--model",
        "claude-opus-4-6",
    ],
    "gemini": ["gemini", "-p", "{prompt}", "--model", "gemini-3-pro-preview", "--yolo"],
}


def get_config() -> Config:
    """Load config from jobs.json."""
    data = json.loads(JOBS_FILE.read_text())
    return Config(**data)


def get_jobs() -> list[JobConfig]:
    """Get all job configs."""
    return get_config().jobs


def setup():
    """Install skills globally via openskills."""
    config = get_config()
    cmd = ["npx", "openskills", "install", config.skills_repo, "--global", "-y"]
    print(f"Installing skills from {config.skills_repo}...")
    subprocess.run(cmd, check=True)
    print("Skills installed.")


def run_job(config: JobConfig, dry_run: bool = False):
    """Run a skill in the target path."""
    if not config.enabled:
        return

    target = Path(config.path)
    prompt = f"/{config.skill}"
    if config.prompt:
        prompt = f"{prompt}\n\n{config.prompt}"
    cmd = [arg.replace("{prompt}", prompt) for arg in PROVIDERS[config.provider]]

    if dry_run:
        print(f"[DRY RUN] Would run {prompt} in {target}")
        print(f"  {' '.join(cmd)}")
        return

    if not target.exists():
        print(f"Path not found: {target}")
        return

    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{config.name}_{config.provider}_{timestamp}.log"

    print(f"Running {config.provider} on {config.name} (/{config.skill})")
    print(f"Log: {log_file}")

    with open(log_file, "w") as lf:
        proc = subprocess.Popen(
            cmd, cwd=target, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in proc.stdout:
            print(line, end="")
            lf.write(line)
            lf.flush()
        proc.wait()

    print(f"Done (exit {proc.returncode})")
