"""
This module contains the settings
"""

import os
import sys
import tempfile
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
    database_url: str = (
        f"sqlite:///{Path.home().joinpath('.annoto').joinpath('db.sqlite3')}"
    )
    debug_routes: bool = True
    jwt_algorithm: str = "HS256"
    jwt_secret: str = "fd232ad1ff70a3a874dda48e857b1ef086e474194ce5d2f8"
    jwt_expiry: int = 60 * 60 * 24  # one day
    engine_connect_args: dict = {}

    class Config:
        """Reads the dotenv file"""

        env_file = f".env.{PYTHON_ENV}"


def initial_settings() -> dict:
    """Initial setting values"""
    if "pytest" in sys.modules:  # Running in test mode
        temp_folder = Path(tempfile.mkdtemp(prefix="annoto"))
        return {
            "database_url": f"sqlite:///{temp_folder.joinpath('test_db.sqlite3')}",
            "engine_connect_args": {"check_same_thread": False},
        }
    return {}


SETTINGS = Settings(**initial_settings())
if SETTINGS.database_url.startswith("postgres://"):
    SETTINGS.database_url = SETTINGS.database_url.replace(
        "postgres://", "postgresql://"
    )
