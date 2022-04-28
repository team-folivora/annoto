"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from mod.src.database import crud
from mod.src.models import user

def test_get_unknown_user_returns_404(client: TestClient) -> None:
    """Test GET /users/42"""
    response = client.get("/users/42")
    assert response.status_code == 404


def test_create_user_with_existing_email(client: TestClient, db) -> None:
    test_user = user.UserCreate(
        username="AnnotoUser#1337",
        password="password",
        email="annoto@team-folivora.com",
        )
    crud.create_user(db, test_user)
    response = client.post(
        "/users/",
        json=test_user.dict(),
    )
    assert response.status_code == 400


def test_create_user(client: TestClient, db) -> None:
    test_user = user.UserCreate(
        username="AnnotoUser#1337",
        password="password",
        email="annoto@team-folivora.com",
    )
    response = client.post(
        "/users/",
        json=test_user.dict(),
    )
    assert response.status_code == 200
    assert crud.get_user_by_email(db, test_user.email).id == response.json()["id"]
