"""Routes for images and annotations"""

from datetime import datetime
import os
import random
import re

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse

from mod.src.models.annotation import (
    Annotation,
    AnnotationData,
    HashMismatch,
    InvalidProof,
    InvalidUsername,
)
from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/tasks/{task_id}",
    tags=["tasks"],
)


@ROUTER.get(
    "/next",
    responses={
        200: {"content": {"text/plain": {"example": "ecg_1.png"}}},
        404: {"description": "No more images to annotate"},
    },
    operation_id="get_next_image",
)
async def get_next_image(
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
) -> str:
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
    random.seed(datetime.now())
    return random.choice(images)


@ROUTER.get(
    "/{src}",
    response_class=FileResponse,
    responses={
        200: {"content": {"image/*": {"schema": {"type": "file", "format": "binary"}}}},
        404: {"description": "File not found"},
    },
    operation_id="get_image",
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
        406: {"description": "Provided username is not valid!"},
    },
    operation_id="save_annotation",
)
async def save_annotation(
    annotation_data: AnnotationData,
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
    src: str = Path(..., example="sloth.jpg"),
) -> None:
    """Saves the annotation for the specified image"""

    annotation = Annotation.from_data(
        annotation_data=annotation_data, src=f"{task_id}/{src}"
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
    except InvalidUsername:
        raise HTTPException(
            status_code=406,
            detail="Provided username is not valid!",
        ) from None
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not Found!") from None
