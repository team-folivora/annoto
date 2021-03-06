"""
Module for integration tests
"""

import json
import time

from mod.src.settings import SETTINGS
from mod.tests.integration.conftest import ManagedTestClient


def test_get_image(client: ManagedTestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb/sloth.jpg"""
    client.authorize()
    response = client.get(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_get_unknown_image_returns_404(client: ManagedTestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb/unknown_image.jpg raises HttpException 404"""
    client.authorize()
    response = client.get(
        "/tasks/ecg-qrs-classification-physiodb/unknown_image.jpg",
    )
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_post_image(client: ManagedTestClient) -> None:
    """Test POST /tasks/ecg-qrs-classification-physiodb/sloth.jpg"""
    client.authorize()
    current_time = int(time.time())
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
        json={
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
            "is_trained": True,
        },
    )
    assert response.status_code == 204

    annotation_file = SETTINGS.data_folder.joinpath(
        "ecg-qrs-classification-physiodb/sloth.jpg.annotation.json"
    )
    assert annotation_file.is_file()
    with open(annotation_file, "r", encoding="utf8") as file:
        assert json.loads(file.read()) == {
            "src": "ecg-qrs-classification-physiodb/sloth.jpg",
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Prof. Dr. Med",
            "is_attentive": True,
            "fullname": "Prof. Dr. Folivora",
            "is_trained": True,
            "timestamp": current_time,
        }


def test_post_unknown_image_returns_404(client: ManagedTestClient) -> None:
    """
    Test POST /tasks/ecg-qrs-classification-physiodb/unknown_image.jpg
    raises HttpException 404
    """
    client.authorize()
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/unknown_image.jpg",
        json={
            "label": "foo",
            "hash": "unknown",
            "competency": "Dr. Dr. med",
            "is_attentive": True,
            "is_trained": True,
        },
    )
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_post_image_wrong_hash_returns_400(client: ManagedTestClient) -> None:
    """Test POST /tasks/ecg-qrs-classification-physiodb/sloth.jpg raises HttpException 400"""
    client.authorize()
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
        json={
            "label": "foo",
            "hash": "wrong",
            "competency": "Dr. Dr. med",
            "is_attentive": True,
            "is_trained": True,
        },
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"


def test_post_image_with_invalid_proof_returns_428(client: ManagedTestClient) -> None:
    """Test POST /tasks/ecg-qrs-classification-physiodb/sloth.jpg raises HttpException 428"""
    client.authorize()
    response = client.post(
        "/tasks/ecg-qrs-classification-physiodb/sloth.jpg",
        json={
            "label": "foo",
            "hash": "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
            "competency": "Dr. Dr. med",
            "is_attentive": False,
            "is_trained": False,
        },
    )
    assert response.status_code == 428
    assert response.headers["content-type"] == "application/json"


def test_get_next_image(client: ManagedTestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb/next"""
    client.authorize()
    response = client.get(
        "/tasks/ecg-qrs-classification-physiodb/next",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    image_id = response.text
    assert (
        client.get(
            f"/tasks/ecg-qrs-classification-physiodb/{image_id}",
        ).status_code
        == 200
    )


def test_get_next_image_returns_404_if_all_annotated(client: ManagedTestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb/next raises HTTPException 404"""
    client.authorize()
    task_folder = SETTINGS.data_folder.joinpath("ecg-qrs-classification-physiodb")
    with open(task_folder.joinpath("ecg_1.png.annotation.json"), "w", encoding="utf-8"):
        pass
    with open(task_folder.joinpath("ecg_2.png.annotation.json"), "w", encoding="utf-8"):
        pass
    with open(task_folder.joinpath("ecg_3.png.annotation.json"), "w", encoding="utf-8"):
        pass
    with open(task_folder.joinpath("sloth.jpg.annotation.json"), "w", encoding="utf-8"):
        pass
    response = client.get(
        "/tasks/ecg-qrs-classification-physiodb/next",
    )
    assert response.status_code == 404
