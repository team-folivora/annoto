
import os
import random
import re

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import FileResponse, PlainTextResponse
from mod.src.app import get_db

from mod.src.models.annotation import (
    Annotation,
    AnnotationData,
    HashMismatch,
    InvalidProof,
    InvalidUsername,
)
from mod.src.settings import SETTINGS
from sqlalchemy.orm import Session
from mod.src.database import crud, models, schemas

ROUTER = APIRouter(
    prefix="/users",
    tags=["users"],
)

@ROUTER.get("/{user_id}", response_model=schemas.User,
    responses={
         404: {"description": "User not found"},
    },
    operation_id="create_user",)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

