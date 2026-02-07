"""Pydantic models for configuration."""

from typing import Literal

from pydantic import BaseModel


class ScheduleConfig(BaseModel):
    """Schedule configuration."""

    cron: str
    times: int = 1


class JobConfig(BaseModel):
    """Job configuration."""

    name: str
    skill: str
    path: str
    prompt: str = ""
    enabled: bool = False
    provider: Literal["claude", "gemini"] = "claude"
    schedule: ScheduleConfig

    model_config = {"extra": "forbid"}


class Config(BaseModel):
    """Top-level configuration."""

    skills_repo: str = "guan404ming/claude-code-skills"
    jobs: list[JobConfig]
