"""
Module for integration tests
"""


from mod.src.settings import SETTINGS
from mod.tests.integration.conftest import ManagedTestClient


def test_multiple_tasks_exist_returns_all(client: ManagedTestClient) -> None:
    """Fetching multiple tasks should return a list of that tasks"""
    client.authorize()
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "ecg-qrs-classification-physiodb",
            "description": "Labeling the QRS complex of Physionet ECGs",
            "labels": [
                "Atrial fibrillation",  # pylint: disable=duplicate-code
                "Normal sinus rhythm",
                "Ventricular tachycardia",
                "Noise",
                "Other",
            ],
        },
        {
            "description": "Labeling Pose of Pressure Mat Data from SLP",
            "id": "pressure-mat-pose-estimation-slp",
            "labels": ["Supine", "Left", "Right"],
        },
    ]


def test_no_tasks_exist_returns_empty_list(client: ManagedTestClient) -> None:
    """Tests whether an empty list is returned when no tasks are available"""
    client.authorize()
    with open(
        SETTINGS.data_folder.joinpath("tasks.json"), "w", encoding="utf-8"
    ) as file:
        file.write("[]")
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_task_exists_returns_the_task(client: ManagedTestClient) -> None:
    """Test that a task is returned when it exists"""
    client.authorize()
    response = client.get("/tasks/ecg-qrs-classification-physiodb")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    task = response.json()
    assert task["id"] == "ecg-qrs-classification-physiodb"
    assert task["description"] == "Labeling the QRS complex of Physionet ECGs"
    assert "Noise" in task["labels"]


def test_task_doenst_exist_returns_404(client: ManagedTestClient) -> None:
    """Test that a 404 is returned when the task does not exist"""
    client.authorize()
    response = client.get("/tasks/unknown")
    assert response.status_code == 404
