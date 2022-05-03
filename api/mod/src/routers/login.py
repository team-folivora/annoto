"""Routes for login"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mod.src.database.database import get_db as DB
from mod.src.database.db_models import DBUser
from mod.src.models.login import LoginData

ROUTER = APIRouter(
    prefix="/login",
    tags=["login"],
)


@ROUTER.post(
    "/",
    status_code=204,
    responses={
        401: {"description": "Failed to validate login"},
    },
    operation_id="login",
)
async def login(
    login_data: LoginData,
    db: Session = Depends(DB),
) -> None:
    """Validate login via username and password"""
    user = DBUser.get_by_username(db, login_data.username)
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(status_code=401, detail="Failed to validate login")
