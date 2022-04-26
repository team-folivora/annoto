"""
This module defines the FastAPI application server
"""

from fastapi import FastAPI
from fastapi_restful import Api
from starlette.middleware.cors import CORSMiddleware
from mod.src.database import models

from mod.src.routers import debug, images, tasks

from mod.src.database.database import SessionLocal, engine
from .settings import SETTINGS

models.Base.metadata.create_all(bind=engine)

APP = FastAPI()
API = Api(APP)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

APP.include_router(tasks.ROUTER)
APP.include_router(images.ROUTER)

if SETTINGS.debug_routes:
    APP.include_router(debug.ROUTER)
