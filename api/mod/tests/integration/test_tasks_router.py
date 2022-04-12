"""
Module for integration tests
"""

from fastapi.testclient import TestClient


def test_get_tasks(client: TestClient) -> None:
    """Test GET /tasks"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == ["ecg-qrs-classification-physiodb"]


def test_get_task(client: TestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb"""
    response = client.get("/tasks/ecg-qrs-classification-physiodb")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    task = response.json()
    assert task["id"] == "ecg-qrs-classification-physiodb"
    assert task["description"] == "Labeling the QRS complex of Physionet ECGs"
    assert "Noise" in task["labels"]


def test_get_unknown_task_returns_404(client: TestClient) -> None:
    """Test GET /tasks/unknown"""
    response = client.get("/tasks/unknown")
    assert response.status_code == 404
