"""
This module defines the FastAPI application server
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mod.src.routers import debug, login, ping, samples, tasks, users

from .settings import SETTINGS

APP = FastAPI()

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

APP.include_router(tasks.ROUTER)
APP.include_router(samples.ROUTER)
APP.include_router(users.ROUTER)
APP.include_router(login.ROUTER)
APP.include_router(ping.ROUTER)

if SETTINGS.debug_routes:
    APP.include_router(debug.ROUTER)
