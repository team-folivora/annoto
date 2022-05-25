"""Routes for images and annotations"""

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from mod.src.models.task import TaskType
from mod.src.routers.tasks import TaskTypeGuard

from mod.src.auth.auth_bearer import JWTBearer
from mod.src.auth.auth_handler import decodeJWT
from mod.src.models.annotation import (
    HashMismatch,
    InvalidProof,
    SpecificAnnotationData,
)
from mod.src.models.task import BaseTask
from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/tasks/{task_id}",
    tags=["tasks"],
)


@ROUTER.get(
    "/next",
    response_class=PlainTextResponse,
    responses={
        200: {
            "content": {
                "text/plain": {
                    "example": "ecg_1.png",
                }
            }
        },
        404: {"description": "No more samples to annotate"},
    },
    operation_id="get_next_sample",
    dependencies=[Depends(JWTBearer())],
)
async def get_next_sample(
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
) -> PlainTextResponse:
    """Get the sample that should be annotated"""
    task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
    task = BaseTask.load_from_file(task_file)
    sample = task.next_sample()
    if not sample:
        raise HTTPException(status_code=404, detail="No more samples to annotate")
    return PlainTextResponse(sample)


@ROUTER.get(
    "/{src}",
    response_class=FileResponse,
    responses={
        200: {"content": {"image/*": {"schema": {"type": "file", "format": "binary"}}}},
        404: {"description": "File not found"},
    },
    operation_id="get_image",
    dependencies=[Depends(JWTBearer()), Depends(TaskTypeGuard(TaskType.IMAGE_CLASSIFICATION))],
)
async def get_image(
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
    src: str = Path(..., example="sloth.jpg"),
) -> FileResponse:
    """Get the image that should be annotated"""
    image_file = SETTINGS.data_folder.joinpath(task_id).joinpath(src)
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(image_file))


@ROUTER.post(
    "/{sample_id}",
    status_code=204,
    responses={
        404: {"description": "File not found!"},
        400: {
            "description": "Hash values of the annotation and the local source do not match!"
        },
        428: {"description": "Provided proofs are not valid!"},
    },
    operation_id="save_annotation",
    dependencies=[Depends(JWTBearer())],
)
async def save_annotation(
    annotation_data: SpecificAnnotationData,
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
    sample_id: str = Path(..., example="sloth.jpg"),
    jwt: HTTPAuthorizationCredentials = Depends(JWTBearer()),
) -> None:
    """Saves the annotation for the specified sample"""

    jwt = decodeJWT(jwt.credentials)
    if not jwt:
        raise HTTPException(status_code=500)

    if not annotation_data.proofs_are_valid():
        raise HTTPException(
            status_code=428,
            detail="Provided proofs are not valid!",
        ) from None

    task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
    task = BaseTask.load_from_file(task_file)

    try:
        task.save_annotation(sample_id, annotation_data, jwt)
    except HashMismatch:
        raise HTTPException(
            status_code=400,
            detail="Hash values of the provided annotation and the local source do not match!",
        ) from None
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not Found!") from None
