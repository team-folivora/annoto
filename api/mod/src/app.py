"""
This module defines the FastAPI application server
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi_restful import Api
from starlette.middleware.cors import CORSMiddleware

from mod.src.models.annotation import (
    AnnotationData,
    Annotation,
    HashMismatch,
    InvalidProof,
)

from .settings import SETTINGS

APP = FastAPI()
API = Api(APP)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


@APP.get(
    "/images/{src}",
    response_class=FileResponse,
    responses={
        200: {"content": {"image/*": {"schema": {"type": "file", "format": "binary"}}}},
        404: {"description": "File not found"},
    },
    operation_id="get_image",
)
async def get_image(src: str) -> FileResponse:
    """Get the image that should be annotated"""
    image_file = SETTINGS.data_folder.joinpath(src)
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(image_file))


@APP.post(
    "/images/{src}",
    status_code=204,
    responses={
        404: {"description": "File not found!"},
        400: {
            "description":
            "Hash values of the provided annotation and the local source do not match!"
        },
        420: {"description": "Provided proofs are not valid!"},
    },
    operation_id="save_annotation",
)
async def save_annotation(src: str, annotation_data: AnnotationData) -> None:
    """Saves the annotation for the specified image"""

    annotation = Annotation.from_data(annotation_data=annotation_data, src=src)

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
