"""
Module for integration tests
"""

import json

import pytest
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from mod.src.app import APP
from mod.src.settings import SETTINGS


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


def test_post_image_with_invalid_proof_return_428(client: TestClient) -> None:
    """Test POST /images/sloth.jpg raises HttpException 428"""
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
    assert response.status_code == 428
    assert response.headers["content-type"] == "application/json"


def assert_heading(page: BeautifulSoup, index: str) -> None:
    """Helper method to assert page heading"""
    assert page.body.find("h1").text == f"Index of {index}"


def assert_entry(page: BeautifulSoup, href: str, text: str) -> None:
    """Helper method to assert the page has a link to an entry"""
    assert page.body.find("a", attrs={"href": href}).text.strip() == text


def test_get_datafolder(client: TestClient) -> None:
    """Test GET /debug/data"""
    response = client.get(
        "/debug/data",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/")
    assert_entry(page, "/debug/data/subfolder", "subfolder/")
    assert_entry(page, "/debug/data/sloth.jpg", "sloth.jpg")


def test_get_datafolder_sloth(client: TestClient) -> None:
    """Test GET /debug/data/sloth.jpg"""
    response = client.get(
        "/debug/data/sloth.jpg",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_get_datafolder_subfolder(client: TestClient) -> None:
    """Test GET /debug/data/subfolder"""
    response = client.get(
        "/debug/data/subfolder",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/subfolder/")
    assert_entry(page, "/debug/data", "..")
    assert_entry(page, "/debug/data/subfolder/subsubfolder", "subsubfolder/")
    assert_entry(page, "/debug/data/subfolder/loremipsum.txt", "loremipsum.txt")


def test_get_datafolder_subfolder_loremipsum(client: TestClient) -> None:
    """Test GET /debug/data/subfolder/loremipsum.txt"""
    response = client.get(
        "/debug/data/subfolder/loremipsum.txt",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"


def test_get_datafolder_subfolder_subsubfolder(client: TestClient) -> None:
    """Test GET /debug/data/subfolder/subsubfolder"""
    response = client.get(
        "/debug/data/subfolder/subsubfolder",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/subfolder/subsubfolder/")
    assert_entry(page, "/debug/data/subfolder", "..")


def test_get_datafolder_unknown_file_returns_404(client: TestClient) -> None:
    """Test GET /debug/data/unknown_file.txt"""
    response = client.delete(
        "/debug/data/unknown_file.txt",
    )
    assert response.status_code == 404


def test_delete_datafolder_file(client: TestClient) -> None:
    """Test DELETE /debug/data/sloth.jpg"""
    response = client.delete(
        "/debug/data/sloth.jpg",
    )
    assert response.status_code == 204
    assert not SETTINGS.data_folder.joinpath("sloth.jpg").exists()
    assert SETTINGS.data_folder.joinpath("subfolder").exists()


def test_delete_datafolder_directory(client: TestClient) -> None:
    """Test DELETE /debug/data/subfolder"""
    response = client.delete(
        "/debug/data/subfolder",
    )
    assert response.status_code == 204
    assert not SETTINGS.data_folder.joinpath("subfolder").exists()
    assert SETTINGS.data_folder.joinpath("sloth.jpg").exists()


def test_delete_datafolder_unknown_file_returns_404(client: TestClient) -> None:
    """Test DELETE /debug/data/unknown_file.txt"""
    response = client.delete(
        "/debug/data/unknown_file.txt",
    )
    assert response.status_code == 404


def test_delete_datafolder_root_fails(client: TestClient) -> None:
    """Test DELETE /debug/data/"""
    response = client.delete(
        "/debug/data/",
    )
    assert response.status_code == 400
