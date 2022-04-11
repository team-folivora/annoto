"""Provides fixtures to the tests"""

import shutil
import tempfile
from pathlib import Path
from typing import Generator
from fastapi.testclient import TestClient

import pytest
from mod.src.app import APP

from mod.src.settings import SETTINGS


@pytest.fixture()
def client() -> TestClient:
    """Get a client for testing the api"""
    return TestClient(APP)


@pytest.fixture(scope="function", autouse=True)
def session() -> Generator:
    """Manages testing session"""
    SETTINGS.data_folder = Path(tempfile.mkdtemp(prefix="annoto"))

    dst = SETTINGS.data_folder
    src = Path.cwd().joinpath("mod").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)

    yield SETTINGS

    shutil.rmtree(SETTINGS.data_folder)
