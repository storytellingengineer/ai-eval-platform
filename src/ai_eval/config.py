"""Environment-backed configuration for the evaluation platform."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Minimal runtime settings used by the foundation release."""

    environment: str = os.getenv("AI_EVAL_ENV", "development")
    log_level: str = os.getenv("AI_EVAL_LOG_LEVEL", "INFO")
