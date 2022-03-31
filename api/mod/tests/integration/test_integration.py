"""
Module for integration tests
"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from mod.src.app import APP
from mod.src.settings import SETTINGS


@pytest.fixture(scope="session", autouse=True)
def session() -> Generator:
    """Manages testing session"""
    SETTINGS.data_folder = Path(tempfile.mkdtemp(prefix="annoto"))
    SETTINGS.testing = True

    dst = SETTINGS.data_folder
    src = Path.cwd().joinpath("mod").joinpath("tests").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)

    yield SETTINGS

    shutil.rmtree(SETTINGS.data_folder)


@pytest.fixture()
def client() -> TestClient:
    """Get a client for testing the api"""
    return TestClient(APP)


def test_get_image(client: TestClient) -> None:
    """Test GET /image"""
    response = client.get("/image")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_post_image(client: TestClient) -> None:
    """Test POST /image"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
        },
    )
    assert response.status_code == 204

    annotation_file = SETTINGS.data_folder.joinpath("sloth.jpg.annotation.json")
    assert annotation_file.is_file()
    with open(annotation_file, encoding="utf8") as file:
        assert json.loads(file.read()) == {
            "label": "foo",
            "src": "sloth.jpg",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
        }
