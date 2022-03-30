"""
This module defines the FastAPI application server
"""

import hashlib
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
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


@APP.post("/images/{src}")
async def save_annotation(src: str, data: dict) -> Response:
    """Saves the annotation for the specified image"""
    annotation = {
        "src": src,
        "label": data["label"],
    }

    image_file = SETTINGS.data_folder.joinpath(src)
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    with open(image_file, "rb") as f:
        r = f.read()
        annotation["hash"] = hashlib.sha256(r).hexdigest()

    annotation_file = SETTINGS.data_folder.joinpath(f"{src}.annnotation.json")
    with open(annotation_file, "w") as f:
        f.write(json.dumps(annotation, indent=4))

    return Response(status_code=204)
