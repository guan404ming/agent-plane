"""Pydantic models for configuration."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class ScheduleConfig(BaseModel):
    """Schedule configuration."""

    cron: str
    times: int = 1


class ProjectConfig(BaseModel):
    """Project configuration."""

    name: str
    path: str
    enabled: bool = False
    provider: Literal["claude", "gemini"] = "claude"
    schedule: ScheduleConfig
    dir: Path = Field(default=None, exclude=True)

    model_config = {"extra": "forbid"}
