"""
Module for integration tests
"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from bs4 import BeautifulSoup
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
            "competency": "Prof. Dr. Med",
        }


def test_post_unknown_image_returns_404(client: TestClient) -> None:
    """Test POST /images/unknown_image.jpg raises HttpException 404"""
    response = client.post(
        "/images/unknown_image.jpg",
        json={
            "label": "foo",
            "hash": "unknown",
        },
    )
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_post_image_wrong_hash_returns_400(client: TestClient) -> None:
    """Test POST /images/sloth.jpg raises HttpException 400"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "label": "foo",
            "hash": "wrong",
        },
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"


def assert_heading(page: BeautifulSoup, index: str) -> None:
    """Helper method to assert page heading"""
    assert page.body.find("h1").text == f"Index of {index}"


def assert_link(page: BeautifulSoup, href: str, text: str) -> None:
    """Helper method to assert page link"""
    assert page.body.find("a", attrs={"href": href}).text.strip() == text


def test_get_datafolder(client: TestClient) -> None:
    """Test GET /data"""
    response = client.get(
        "/data",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/")
    assert_link(page, "/data/subfolder", "subfolder/")
    assert_link(page, "/data/sloth.jpg", "sloth.jpg")


def test_get_datafolder_sloth(client: TestClient) -> None:
    """Test GET /data/sloth.jpg"""
    response = client.get(
        "/data/sloth.jpg",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_get_datafolder_subfolder(client: TestClient) -> None:
    """Test GET /data/subfolder"""
    response = client.get(
        "/data/subfolder",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/subfolder/")
    assert_link(page, "/data", "..")
    assert_link(page, "/data/subfolder/subsubfolder", "subsubfolder/")
    assert_link(page, "/data/subfolder/loremipsum.txt", "loremipsum.txt")


def test_get_datafolder_subfolder_loremipsum(client: TestClient) -> None:
    """Test GET /data/subfolder/loremipsum.txt"""
    response = client.get(
        "/data/subfolder/loremipsum.txt",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"


def test_get_datafolder_subfolder_subsubfolder(client: TestClient) -> None:
    """Test GET /data/subfolder/subsubfolder"""
    response = client.get(
        "/data/subfolder/subsubfolder",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/subfolder/subsubfolder/")
    assert_link(page, "/data/subfolder", "..")
