"""
Module for integration tests
"""

import json

from fastapi.testclient import TestClient

from mod.src.settings import SETTINGS


def test_get_image(client: TestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb/sloth.jpg"""
    response = client.get("/tasks/ecg-qrs-classification-physiodb/sloth.jpg")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_get_unknown_image_returns_404(client: TestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb/unknown_image.jpg raises HttpException 404"""
    response = client.get("/tasks/ecg-qrs-classification-physiodb/unknown_image.jpg")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_post_image(client: TestClient) -> None:
    """Test POST /tasks/ecg-qrs-classification-physiodb/sloth.jpg"""
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
        json={
            "src": "ecg-qrs-classification-physiodb/sloth.jpg",
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
        },
    )
    assert response.status_code == 204

    annotation_file = SETTINGS.data_folder.joinpath(
        "ecg-qrs-classification-physiodb/sloth.jpg.annotation.json"
    )
    assert annotation_file.is_file()
    with open(annotation_file, encoding="utf8") as file:
        assert json.loads(file.read()) == {
            "src": "ecg-qrs-classification-physiodb/sloth.jpg",
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
        }


def test_post_unknown_image_returns_404(client: TestClient) -> None:
    """
    Test POST /tasks/ecg-qrs-classification-physiodb/unknown_image.jpg
    raises HttpException 404
    """
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/unknown_image.jpg",
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
    """Test POST /tasks/ecg-qrs-classification-physiodb/sloth.jpg raises HttpException 400"""
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
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
    """Test POST /tasks/ecg-qrs-classification-physiodb/sloth.jpg raises HttpException 428"""
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
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
