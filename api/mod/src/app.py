"""
This module defines the FastAPI application server
"""

import hashlib
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi_restful import Api
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

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


class Annotation(BaseModel):
    """
    An annotation of a file

    Attributes
        src             name of the annotated file
        label           label the file [src] should be annotated with
        hash            hash of the file
        competency      the competencies the annotator has
        is_attentive    whether the annotator said that he is attentive
    """

    src: Optional[str]
    label: str
    hash: str
    competency: str
    is_attentive: bool

    @property
    def absolute_src(self) -> Path:
        """Returns the absolute path to the annotated file"""
        if not self.src:
            raise AttributeError("No data file specified")
        return SETTINGS.data_folder.joinpath(self.src)

    def file_exists(self) -> bool:
        """Returns whether the annotated file exists"""
        return self.absolute_src.is_file()

    def hash_is_valid(self) -> bool:
        """Returns whether the hash of the annotated file matches"""
        with open(self.absolute_src, "rb") as file:
            local_hash = hashlib.sha256(file.read()).hexdigest()
        return local_hash == self.hash

    def proofs_are_valid(self) -> bool:
        """Checks whether the proofs of the annotator are all valid"""
        return self.is_attentive

    def save(self) -> None:
        """Saves this annotation to the filesystem"""
        annotation_file = SETTINGS.data_folder.joinpath(f"{self.src}.annotation.json")
        with open(annotation_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.__dict__, indent=4))


@APP.post(
    "/images/{src}",
    status_code=204,
    responses={
        404: {"description": "File not found"},
        400: {},
        420: {"Provided proofs are not valid"},
    },
    operation_id="save_annotation",
)
async def save_annotation(src: str, annotation: Annotation) -> None:
    """Saves the annotation for the specified image"""
    annotation.src = src

    if not annotation.file_exists():
        raise HTTPException(status_code=404, detail="File not found!")

    if not annotation.hash_is_valid():
        raise HTTPException(
            status_code=400,
            detail="Hash values of the provided annotation and the local source do not match!",
        )

    if not annotation.proofs_are_valid():
        raise HTTPException(status_code=420, detail="Provided proofs are not valid")

    annotation.save()
