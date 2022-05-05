"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from mod.src.database.db_models import DBUser
from mod.src.models.user import CreateUserRequest


def test_get_user_returns_correct_user(
    client: TestClient,
) -> None:
    """Test GET /users/1"""
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "team@folivora.online"


def test_get_unknown_user_returns_404(client: TestClient) -> None:
    """Test GET /users/42"""
    response = client.get("/users/42")
    assert response.status_code == 404


def test_create_user_with_existing_email_returns_400(client: TestClient) -> None:
    """Test POST /users/ with existing email"""
    user = CreateUserRequest(
        fullname="Prof. Nr. 2", email="team@folivora.online", password="asdfasdf"
    )
    response = client.post(
        "/users/",
        json=user.dict(),
    )
    assert response.status_code == 400


def test_create_user(client: TestClient, db: Session) -> None:
    """Test POST /users/ with new user"""
    user = CreateUserRequest(
        fullname="Prof. Dr. Perry",
        password="brrrrrrr",
        email="perry@folivora.online",
    )
    response = client.post(
        "/users/",
        json=user.dict(),
    )
    assert response.status_code == 200
    created_user = DBUser.get_by_email(db, email=user.email)
    assert created_user is not None
    assert created_user.id == response.json()["id"]
