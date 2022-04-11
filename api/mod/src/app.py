"""
This module defines the FastAPI application server
"""

import os
import shutil
from pathlib import PurePath
from typing import Union

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi_restful import Api
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import _TemplateResponse

from mod.src.models.annotation import (
    Annotation,
    AnnotationData,
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

TEMPLATE_DIRECTORY = domain_template_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)
TEMPLATES = Jinja2Templates(TEMPLATE_DIRECTORY)


@APP.get(
    "/images/{src}",
    response_class=FileResponse,
    responses={
        200: {"content": {"image/*": {"schema": {"type": "file", "format": "binary"}}}},
        404: {"description": "File not found"},
    },
    operation_id="get_image",
)
async def get_image(
    src: str = Path(..., example="sloth.jpg"),
) -> FileResponse:
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
            "description": "Hash values of the annotation and the local source do not match!"
        },
        420: {"description": "Provided proofs are not valid!"},
    },
    operation_id="save_annotation",
)
async def save_annotation(
    annotation_data: AnnotationData,
    src: str = Path(..., example="sloth.jpg"),
) -> None:
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


def path_url(path: PurePath) -> str:
    """Get the url to a path inside the data folder (~/.annoto)"""

    url_path = str(path.relative_to(SETTINGS.data_folder)).replace(os.path.sep, "/")
    return f"/debug/data/{url_path}" if url_path != "." else "/debug/data"


if SETTINGS.debug_routes:

    @APP.get(
        "/debug/data/{path:path}",
        response_class=FileResponse,
        responses={
            200: {
                "content": {
                    "*": {"schema": {"type": "file", "format": "binary"}},
                    "text/html": {},
                },
            },
            404: {"description": "File not found"},
        },
    )
    async def serve_data_folder(
        request: Request, path: str
    ) -> Union[FileResponse, _TemplateResponse]:
        """Serves the data folder (~/.annoto)"""

        path = SETTINGS.data_folder.joinpath(path)

        if path.is_file():
            return FileResponse(path)

        if path.is_dir():
            entries = list(
                map(
                    lambda e: {
                        "name": f"{e}/" if path.joinpath(e).is_dir() else e,
                        "url": path_url(path.joinpath(e)),
                    },
                    os.listdir(path),
                )
            )

            base = f"{path_url(path)[len('/debug/data') :]}/"
            if base != "/":
                entries.insert(
                    0,
                    {
                        "name": "..",
                        "url": path_url(path.parent),
                    },
                )

            return TEMPLATES.TemplateResponse(
                "list_directory.html",
                {
                    "request": request,
                    "entries": entries,
                    "base": base,
                },
            )

        raise HTTPException(status_code=404, detail="File not found")

    @APP.delete(
        "/debug/data/{path:path}",
        status_code=204,
        responses={
            404: {"description": "File not found"},
            400: {},
        },
    )
    async def delete_from_data_folder(path: str) -> None:
        """Delete from the data folder (~/.annoto)"""

        path = SETTINGS.data_folder.joinpath(path)
        if path == SETTINGS.data_folder:
            raise HTTPException(status_code=400)
        if path.is_file():
            os.remove(path)
        elif path.is_dir():
            shutil.rmtree(path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
