"""
This module defines the FastAPI application server
"""

import hashlib
import json
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi_restful import Api

from .settings import SETTINGS

APP = FastAPI()
API = Api(APP)


@APP.get("/image")
async def get_image() -> FileResponse:
    """Get the image that should be annotated"""
    image_file = SETTINGS.data_folder.joinpath("sloth.jpg")
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(image_file))


class Annotation(BaseModel):
    """Stores an annotation"""

    label: str


@APP.post("/images/{src}", status_code=204)
async def save_annotation(src: str, annotation: Annotation) -> None:
    """Saves the annotation for the specified image"""
    annotation = {
        "src": src,
        "label": annotation.label,
    }

    image_file = SETTINGS.data_folder.joinpath(src)
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    with open(image_file, "rb") as file:
        annotation["hash"] = hashlib.sha256(file.read()).hexdigest()

    annotation_file = SETTINGS.data_folder.joinpath(f"{src}.annnotation.json")
    with open(annotation_file, "w", encoding="utf-8") as file:
        file.write(json.dumps(annotation, indent=4))
