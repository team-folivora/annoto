"""
This module defines the FastAPI application server
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi_restful import Api

from .settings import SETTINGS

APP = FastAPI()
API = Api(APP)


@APP.get("/image")
async def get_image() -> FileResponse:
    """Get the image that should be annotated"""
    image_path = Path(SETTINGS.data_folder).joinpath("sloth.jpg")
    return FileResponse(str(image_path))
