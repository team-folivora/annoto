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

    dst = SETTINGS.data_folder
    src = Path.cwd().joinpath("mod").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)

    yield SETTINGS

    shutil.rmtree(SETTINGS.data_folder)


@pytest.fixture()
def client() -> TestClient:
    """Get a client for testing the api"""
    return TestClient(APP)


def test_get_image(client: TestClient) -> None:
    """Test GET /images/sloth.jpg"""
    response = client.get("/images/sloth.jpg")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_get_unknown_image_returns_404(client: TestClient) -> None:
    """Test GET /images/unknown_image.jpg raises HttpException 404"""
    response = client.get("/images/unknown_image.jpg")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_post_image(client: TestClient) -> None:
    """Test POST /images/sloth.jpg"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "src": "sloth.jpg",
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
        },
    )
    assert response.status_code == 204

    annotation_file = SETTINGS.data_folder.joinpath("sloth.jpg.annotation.json")
    assert annotation_file.is_file()
    with open(annotation_file, encoding="utf8") as file:
        assert json.loads(file.read()) == {
            "src": "sloth.jpg",
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
        }


def test_post_unknown_image_returns_404(client: TestClient) -> None:
    """Test POST /images/unknown_image.jpg raises HttpException 404"""
    response = client.post(
        "/images/unknown_image.jpg",
        json={
            "src": "unknown_image.jpg",
            "label": "foo",
            "hash": "unknown",
            "competency": "Dr. Dr. med",
            "is_attentive": True,
        },
    )
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_post_image_wrong_hash_returns_400(client: TestClient) -> None:
    """Test POST /images/sloth.jpg raises HttpException 400"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "src": "sloth.jpg",
            "label": "foo",
            "hash": "wrong",
            "competency": "Dr. Dr. med",
            "is_attentive": True,
        },
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"


def test_post_image_with_invalid_proof_return_420(client: TestClient) -> None:
    """Test POST /images/sloth.jpg raises HttpException 420"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "src": "sloth.jpg",
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Dr. Dr. med",
            "is_attentive": False,
        },
    )
    assert response.status_code == 420
    assert response.headers["content-type"] == "application/json"
