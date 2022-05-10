"""Provides fixtures to the tests"""

# isort:block

import tempfile
from pathlib import Path

import alembic
from alembic.config import Config

from mod.src.settings import SETTINGS

temp_folder = Path(tempfile.mkdtemp(prefix="annoto"))
SETTINGS.database_url = f"sqlite:///{temp_folder.joinpath('test_db.sqlite3')}"
SETTINGS.engine_connect_args = {"check_same_thread": False}
config = Config(str(Path.cwd().joinpath("alembic.ini")))
config.set_main_option(
    "script_location", str(Path.cwd().joinpath("mod").joinpath("alembic"))
)
config.set_main_option("sqlalchemy.url", SETTINGS.database_url)
alembic.command.upgrade(config, "head")
from scripts.load_test_data import load as load_test_data

load_test_data()

# isort:block

import shutil
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mod.src.app import APP
from mod.src.database.database import engine, get_db


@pytest.fixture()
def client() -> TestClient:
    """Get a client for testing the api"""
    return TestClient(APP)


@pytest.fixture(autouse=True)
def session() -> Generator:
    """Manages testing session"""
    SETTINGS.data_folder = Path(tempfile.mkdtemp(prefix="annoto"))

    dst = SETTINGS.data_folder
    src = Path.cwd().joinpath("mod").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)

    yield SETTINGS

    shutil.rmtree(SETTINGS.data_folder)


@pytest.fixture(autouse=True)
def db() -> scoped_session:  # type: ignore
    """
    Provides a database session that is scoped to the test function
    and is automatically rolled back after the test
    """
    with engine.begin() as connection:
        with connection.begin() as transaction:
            session = scoped_session(sessionmaker(bind=connection))

            def override_get_db() -> scoped_session:
                return session

            APP.dependency_overrides[get_db] = override_get_db
            yield session
            transaction.rollback()
