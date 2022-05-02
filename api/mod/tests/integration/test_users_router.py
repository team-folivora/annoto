"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from mod.src.database import db_models
from mod.src.models import user


def test_get_user_returns_correct_user(
    client: TestClient, db: Session, user: user.UserCreate
) -> None:
    """Test GET /users/1"""
    db_models.User.create(db=db, user=user)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == user.username


def test_get_unknown_user_returns_404(client: TestClient) -> None:
    """Test GET /users/42"""
    response = client.get("/users/42")
    assert response.status_code == 404


def test_create_user_with_existing_email_returns_400(
    client: TestClient, db: Session, user: user.UserCreate
) -> None:
    """Test POST /users/ with existing email"""
    duplicate_email_test_user = user
    duplicate_email_test_user.username = "AnotherUser"
    db_models.User.create(db=db, user=duplicate_email_test_user)
    response = client.post(
        "/users/",
        json=user.dict(),
    )
    assert response.status_code == 400


def test_create_user_with_existing_username_returns_400(
    client: TestClient, db: Session, user: user.UserCreate
) -> None:
    """Test POST /users/ with existing email"""
    duplicate_username_test_user = user
    duplicate_username_test_user.email = "another@email.com"
    db_models.User.create(db=db, user=duplicate_username_test_user)
    response = client.post(
        "/users/",
        json=user.dict(),
    )
    assert response.status_code == 400


def test_create_user(client: TestClient, db: Session, user: user.UserCreate) -> None:
    """Test POST /users/ with new user"""
    response = client.post(
        "/users/",
        json=user.dict(),
    )
    assert response.status_code == 200
    created_user = db_models.User.get_by_email(db, email=user.email)
    assert created_user is not None
    assert created_user.id == response.json()["id"]
