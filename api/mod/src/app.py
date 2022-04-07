"""
This module defines the FastAPI application server
"""

import hashlib
import json
import os
from functools import wraps
from os import PathLike
from typing import Any, Callable, Coroutine, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi_restful import Api
from mypy_extensions import KwArg, VarArg
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import _TemplateResponse

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
    responses={404: {"description": "File not found"}},
)
async def get_image(src: str) -> FileResponse:
    """Get the image that should be annotated"""
    image_file = SETTINGS.data_folder.joinpath(src)
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(image_file))


class Annotation(BaseModel):
    """An annotation as it is provided by the API"""

    label: str
    hash: str


class StorableAnnotation(Annotation):
    """An annotation as it is stored on disk"""

    src: str
    competency: str


@APP.post(
    "/images/{src}",
    status_code=204,
    responses={
        404: {"description": "File not found"},
        400: {},
    },
)
async def save_annotation(src: str, annotation: Annotation) -> None:
    """Saves the annotation for the specified image"""
    image_file = SETTINGS.data_folder.joinpath(src)
    if not image_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    with open(image_file, "rb") as file:
        local_hash = hashlib.sha256(file.read()).hexdigest()
        if local_hash != annotation.hash:
            raise HTTPException(
                status_code=400,
                detail="Hash values of the provided annotation and the local source do not match!",
            )

    annotation = StorableAnnotation(
        label=annotation.label,
        hash=annotation.hash,
        src=src,
        competency="Prof. Dr. Med",  # e.g. loaded from user database
    )

    annotation_file = SETTINGS.data_folder.joinpath(f"{src}.annotation.json")
    with open(annotation_file, "w", encoding="utf-8") as file:
        file.write(json.dumps(annotation.__dict__, indent=4))


def serving_data_folder_required(
    func: Callable[..., Any]
) -> Callable[[VarArg(Any), KwArg(Any)], Coroutine[Any, Any, Callable[..., Any]]]:
    """Decorator to serve route only if serve_data_folder setting is True"""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Callable[..., Any]:
        if not SETTINGS.serve_data_folder:
            raise HTTPException(status_code=405)
        return await func(*args, **kwargs)

    return wrapper


def path_url(path: PathLike[str]) -> str:
    """Get the url to a path inside the data folder (~/.annoto)"""
    url_path = os.path.relpath(path, SETTINGS.data_folder).replace(os.path.sep, "/")
    return f"/data/{url_path}" if url_path != "." else "/data"


@APP.get(
    "/data/{path:path}",
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
@serving_data_folder_required
async def serve_data_folder(
    request: Request, path: str
) -> Union[FileResponse, _TemplateResponse]:
    """Serves the data folder (~/.annoto)"""

    path = SETTINGS.data_folder.joinpath(path)

    if os.path.isfile(path):
        return FileResponse(path)

    if os.path.isdir(path):
        entries = list(
            map(
                lambda e: {
                    "name": f"{e}/" if os.path.isdir(path.joinpath(e)) else e,
                    "url": path_url(path.joinpath(e)),
                },
                os.listdir(path),
            )
        )

        base = f"{path_url(path)[len('/data') :]}/"
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
