"""Routes for login"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mod.src.database.database import get_db
from mod.src.database.db_models import User
from mod.src.models.login import LoginData

ROUTER = APIRouter(
    prefix="/login",
    tags=["login"],
)


@ROUTER.post(
    "/",
    status_code=204,
    responses={
        400: {"description": "No user found with that username"},
        401: {"description": "Failed to validate login"},
    },
    operation_id="login",
)
async def login(
    login_data: LoginData,
    db: Session = Depends(get_db),
) -> None:
    """Validate login via username and password"""
    user = User.get_by_username(db, login_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="No user found with that username")

    if not user.verify_password(login_data.password):
        raise HTTPException(status_code=401, detail="Failed to validate login")
