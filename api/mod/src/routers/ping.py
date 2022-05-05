"""Routes for login"""


from fastapi import APIRouter, Depends
from mod.src.auth.auth_bearer import JWTBearer

ROUTER = APIRouter(
    prefix="/ping",
    tags=["ping"],
)


@ROUTER.get(
    "/",
    status_code=204,
    operation_id="ping",
    dependencies=[Depends(JWTBearer())],
)
async def ping() -> None:
    return
