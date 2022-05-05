"""Routes for login"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mod.src.auth.auth_handler import signJWT
from mod.src.database.database import get_db as DB
from mod.src.database.db_models import DBUser
from mod.src.models.login import LoginRequest, LoginResponse

ROUTER = APIRouter(
    prefix="/login",
    tags=["login"],
)


@ROUTER.post(
    "/",
    responses={
        401: {"description": "Failed to validate login"},
    },
    response_model=LoginResponse,
    operation_id="login",
)
async def login(login_data: LoginRequest, db: Session = Depends(DB)) -> LoginResponse:
    """Validate login via email and password"""
    user = DBUser.get_by_email(db, login_data.email)
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(status_code=401, detail="Failed to validate login")
    return LoginResponse(access_token=signJWT(user.id, user.fullname))
