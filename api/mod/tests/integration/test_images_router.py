"""
Module for integration tests
"""

import json

from fastapi.testclient import TestClient

from mod.src.settings import SETTINGS


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
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
            "username": "AnnotoUser#1337",
            "is_trained": True,
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
            "username": "AnnotoUser#1337",
            "is_trained": True,
        }


def test_post_unknown_image_returns_404(client: TestClient) -> None:
    """Test POST /images/unknown_image.jpg raises HttpException 404"""
    response = client.post(
        "/images/unknown_image.jpg",
        json={
            "label": "foo",
            "hash": "unknown",
            "competency": "Dr. Dr. med",
            "is_attentive": True,
            "username": "AnnotoUser#1337",
            "is_trained": True,
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
            "competency": "Dr. Dr. med",
            "is_attentive": True,
            "username": "AnnotoUser#1337",
            "is_trained": True,
        },
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"


def test_post_image_with_invalid_proof_returns_428(client: TestClient) -> None:
    """Test POST /images/sloth.jpg raises HttpException 428"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Dr. Dr. med",
            "is_attentive": False,
            "username": "AnnotoUser#1337",
            "is_trained": False,
        },
    )
    assert response.status_code == 428
    assert response.headers["content-type"] == "application/json"


def test_post_image_with_invalid_username_returns_406(client: TestClient) -> None:
    """Test POST /images/sloth.jpg raises HttpException 406"""
    response = client.post(
        "/images/sloth.jpg",
        json={
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Dr. Dr. med",
            "is_attentive": True,
            "username": "",
            "is_trained": True,
        },
    )
    assert response.status_code == 406
    assert response.headers["content-type"] == "application/json"
