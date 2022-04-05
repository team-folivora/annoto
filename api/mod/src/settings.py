"""
This module contains the settings
"""

import os
from pathlib import Path

from pydantic import BaseSettings

PYTHON_ENV = os.getenv("PYTHON_ENV", "development")


class Settings(BaseSettings):
    """Basic settings class"""

    data_folder: Path = Path.home().joinpath(".annoto")

    class Config:
        env_file = f".env.{PYTHON_ENV}"


SETTINGS = Settings()
