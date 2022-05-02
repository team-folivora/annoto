"""Routes for login"""

from fastapi import APIRouter, HTTPException

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
) -> None:
    """Validate login via username and password"""
    if login_data.username != "AnnotoUser#1337" or login_data.password != "test1234":
        raise HTTPException(401)
