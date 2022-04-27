"""
This module defines the FastAPI application server
"""

from fastapi import FastAPI
from fastapi_restful import Api
from starlette.middleware.cors import CORSMiddleware
from mod.src.database import db_models

from mod.src.routers import debug, images, tasks, users

from mod.src.database.database import engine
from .settings import SETTINGS

db_models.Base.metadata.create_all(bind=engine)

APP = FastAPI()
API = Api(APP)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

APP.include_router(tasks.ROUTER)
APP.include_router(images.ROUTER)
APP.include_router(users.ROUTER)

if SETTINGS.debug_routes:
    APP.include_router(debug.ROUTER)
