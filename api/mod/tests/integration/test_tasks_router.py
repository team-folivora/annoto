"""
Module for integration tests
"""


from mod.tests.integration.conftest import ManagedTestClient


def test_get_tasks(client: ManagedTestClient) -> None:
    """Test GET /tasks"""
    client.authorize()
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == ["ecg-qrs-classification-physiodb"]


def test_get_task(client: ManagedTestClient) -> None:
    """Test GET /tasks/ecg-qrs-classification-physiodb"""
    client.authorize()
    response = client.get("/tasks/ecg-qrs-classification-physiodb")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    task = response.json()
    assert task["id"] == "ecg-qrs-classification-physiodb"
    assert task["description"] == "Labeling the QRS complex of Physionet ECGs"
    assert "Noise" in task["labels"]


def test_get_unknown_task_returns_404(client: ManagedTestClient) -> None:
    """Test GET /tasks/unknown"""
    client.authorize()
    response = client.get("/tasks/unknown")
    assert response.status_code == 404
