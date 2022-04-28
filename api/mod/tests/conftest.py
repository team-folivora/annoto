"""Provides fixtures to the tests"""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from mod.src.database.database import get_db

from mod.src.app import APP
from mod.src.settings import SETTINGS
import alembic
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


temp_folder = Path(tempfile.mkdtemp(prefix="annoto"))
SETTINGS.database_url = f"sqlite:///{temp_folder.joinpath('test_db.db')}"

engine = create_engine(
    SETTINGS.database_url, connect_args={"check_same_thread": False}
)


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

@pytest.fixture(scope="session")
def apply_migrations() -> None:
    config = Config(Path.cwd().joinpath("mod").joinpath("alembic.ini"))
    config.set_main_option("script_location", str(Path.cwd().joinpath("mod").joinpath("alembic")))
    config.set_main_option("sqlalchemy.url", SETTINGS.database_url)
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")

@pytest.fixture(autouse=True)
def db(apply_migrations: None):
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))

    def override_get_db():
        yield session

    APP.dependency_overrides[get_db] = override_get_db
    yield session
    transaction.rollback()
    connection.close()
