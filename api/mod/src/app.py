"""
This module defines the FastAPI application server
"""

import random
from datetime import datetime
from fastapi import FastAPI
from fastapi_restful import Api
from starlette.middleware.cors import CORSMiddleware

from mod.src.routers import debug, images, tasks

from .settings import SETTINGS

random.seed(datetime.now())

APP = FastAPI()
API = Api(APP)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

APP.include_router(tasks.ROUTER)
APP.include_router(images.ROUTER)

if SETTINGS.debug_routes:
    APP.include_router(debug.ROUTER)
