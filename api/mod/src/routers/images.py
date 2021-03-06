"""Routes for images and annotations"""

import os
import random
import re
import time

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.security.http import HTTPAuthorizationCredentials

from mod.src.auth.auth_bearer import JWTBearer
from mod.src.auth.auth_handler import decodeJWT
from mod.src.models.annotation import (
    Annotation,
    AnnotationData,
    HashMismatch,
    InvalidProof,
)
from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/tasks/{task_id}",
    tags=["tasks"],
)


@ROUTER.get(
    "/next",
    response_class=PlainTextResponse,
    responses={
        200: {"content": {"text/plain": {"example": "ecg_1.png"}}},
        404: {"description": "No more images to annotate"},
    },
    operation_id="get_next_image",
    dependencies=[Depends(JWTBearer())],
)
async def get_next_image(
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
) -> PlainTextResponse:
    """Get the image that should be annotated"""
    task_folder = SETTINGS.data_folder.joinpath(task_id)
    images = list(
        filter(lambda f: re.match(".*\\.(png|jpg|jpeg)$", f), os.listdir(task_folder))
    )
    images = list(
        filter(
            lambda f: not task_folder.joinpath(f"{f}.annotation.json").exists(), images
        )
    )
    if not images:
        raise HTTPException(status_code=404, detail="No more images to annotate")
    return PlainTextResponse(random.choice(images))


@ROUTER.get(
    "/{src}",
    response_class=FileResponse,
    responses={
        200: {"content": {"image/*": {"schema": {"type": "file", "format": "binary"}}}},
        404: {"description": "File not found"},
    },
    operation_id="get_image",
    dependencies=[Depends(JWTBearer())],
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
    "/{src}",
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
    annotation_data: AnnotationData,
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
    src: str = Path(..., example="sloth.jpg"),
    jwt: HTTPAuthorizationCredentials = Depends(JWTBearer()),
) -> None:
    """Saves the annotation for the specified image"""

    jwt = decodeJWT(jwt.credentials)
    if not jwt:
        raise HTTPException(status_code=500)

    annotation = Annotation.from_data(
        annotation_data=annotation_data,
        src=f"{task_id}/{src}",
        fullname=jwt.fullname,
        timestamp=int(time.time()),
    )

    try:
        annotation.save()
    except HashMismatch:
        raise HTTPException(
            status_code=400,
            detail="Hash values of the provided annotation and the local source do not match!",
        ) from None
    except InvalidProof:
        raise HTTPException(
            status_code=428,
            detail="Provided proofs are not valid!",
        ) from None
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not Found!") from None
