"""
This module contains the settings
"""

import os
from pathlib import Path

from pydantic import BaseSettings

PYTHON_ENV = os.getenv("PYTHON_ENV", "development")


class Settings(BaseSettings):
    """
    Basic settings class. Loads class attributes with the following priority:
    1. env variables
    2. values loaded from dotenv file according to PYTHON_ENV
    3. defaults specified here
    """

    data_folder: Path = Path.home().joinpath(".annoto")
    debug_routes: bool = True

    class Config:
        """Reads the dotenv file"""

        env_file = f".env.{PYTHON_ENV}"


SETTINGS = Settings()
