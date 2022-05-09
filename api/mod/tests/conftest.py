"""Provides fixtures to the tests"""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import alembic
import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mod.src.app import APP
from mod.src.database.database import get_db
from mod.src.settings import SETTINGS


@pytest.fixture(autouse=True)
def session() -> Generator:
    """Manages testing session"""
    SETTINGS.data_folder = Path(tempfile.mkdtemp(prefix="annoto"))

    dst = SETTINGS.data_folder
    src = Path.cwd().joinpath("mod").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)

    yield SETTINGS

    shutil.rmtree(SETTINGS.data_folder)


@pytest.fixture(scope="session", autouse=True)
def db_engine() -> Generator:
    """Creates database engine and migrations to test database"""
    temp_folder = Path(tempfile.mkdtemp(prefix="annoto"))
    SETTINGS.database_url = f"sqlite:///{temp_folder.joinpath('test_db.sqlite3')}"

    engine = create_engine(
        SETTINGS.database_url, connect_args={"check_same_thread": False}
    )
    config = Config(str(Path.cwd().joinpath("alembic.ini")))
    config.set_main_option(
        "script_location", str(Path.cwd().joinpath("mod").joinpath("alembic"))
    )
    config.set_main_option("sqlalchemy.url", SETTINGS.database_url)
    alembic.command.upgrade(config, "head")
    yield engine
    alembic.command.downgrade(config, "base")


@pytest.fixture(autouse=True)
def db(db_engine) -> scoped_session:  # type: ignore
    """
    Provides a database session that is scoped to the test function
    and is automatically rolled back after the test
    """
    with db_engine.begin() as connection:
        with connection.begin() as transaction:
            session = scoped_session(sessionmaker(bind=connection))

            # FIXME load test data appropriately # pylint: disable=W0511

            from mod.src.database.db_models import (  # pylint: disable=import-outside-toplevel
                CreateUserRequest,
                DBUser,
            )

            DBUser.create(
                db=session,
                user=CreateUserRequest(
                    fullname="Prof. Dr. Folivora",
                    password="password",
                    email="team@folivora.online",
                ),
            )

            def override_get_db() -> scoped_session:
                return session

            APP.dependency_overrides[get_db] = override_get_db
            yield session
            transaction.rollback()
