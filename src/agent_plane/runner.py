"""Job runner - load config and execute skills via openskills."""

import json
import os
import smtplib
import subprocess
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

from agent_plane.models import Config, EmailConfig, JobConfig

ROOT_DIR = Path(__file__).parent.parent.parent
JOBS_FILE = ROOT_DIR / "jobs.json"
LOGS_DIR = ROOT_DIR / "logs"

CMD = [
    "claude",
    "-p",
    "{prompt}",
    "--dangerously-skip-permissions",
    "--model",
    "claude-opus-4-6",
]


ENV_FILE = ROOT_DIR / ".env"


def _load_env():
    """Load .env file into os.environ."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def get_config() -> Config:
    """Load config from jobs.json, with smtp_password from .env."""
    _load_env()
    data = json.loads(JOBS_FILE.read_text())
    config = Config(**data)
    if config.email:
        config.email.smtp_user = os.environ.get("SMTP_USER", config.email.smtp_user)
        config.email.smtp_password = os.environ.get(
            "SMTP_PASSWORD", config.email.smtp_password
        )
    return config


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


def send_email(email: EmailConfig, subject: str, body: str):
    """Send email via Gmail SMTP."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email.smtp_user
    msg["To"] = email.to
    with smtplib.SMTP(email.smtp_host, email.smtp_port) as server:
        server.starttls()
        server.login(email.smtp_user, email.smtp_password)
        server.send_message(msg)
    print(f"Email sent to {email.to}")


def run_job(config: JobConfig, dry_run: bool = False):
    """Run a skill in the target path."""
    if not config.enabled:
        return

    target = Path(config.path)
    prompt = f"/{config.skill}"
    if config.prompt:
        prompt = f"{prompt}\n\n{config.prompt}"
    cmd = [arg.replace("{prompt}", prompt) for arg in CMD]

    if dry_run:
        print(f"[DRY RUN] Would run {prompt} in {target}")
        print(f"  {' '.join(cmd)}")
        return

    if not target.exists():
        print(f"Path not found: {target}")
        return

    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{config.name}_{timestamp}.log"

    print(f"Running {config.name} (/{config.skill})")
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

    # Send email notification
    email = get_config().email
    if email:
        status = (
            "completed" if proc.returncode == 0 else f"failed (exit {proc.returncode})"
        )
        lines = log_file.read_text().splitlines()
        log_head = "\n".join(lines[:10])
        log_tail = "\n".join(lines[-10:])
        send_email(
            email,
            subject=f"[agent-plane] {config.name} {status}",
            body=f"Job: {config.name}\nSkill: /{config.skill}\nStatus: {status}\n\n--- Log (first 10 lines) ---\n{log_head}\n\n--- Log (last 10 lines) ---\n{log_tail}",
        )
