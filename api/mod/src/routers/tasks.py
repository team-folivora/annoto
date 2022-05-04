"""Routes for tasks"""

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from mod.src.auth.auth_bearer import JWTBearer
from mod.src.models.task import Task
from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@ROUTER.get(
    "/",
    responses={
        200: {
            "content": {
                "application/json": {"example": ["ecg-qrs-classification-physiodb"]}
            }
        }
    },
    operation_id="get_tasks",
    dependencies=[Depends(JWTBearer())],
)
async def get_tasks() -> List[str]:
    """Get a list of the IDs of all available labelling tasks"""
    tasks_file = SETTINGS.data_folder.joinpath("tasks.json")
    with open(tasks_file, "r", encoding="utf-8") as file:
        return json.load(file)


@ROUTER.get(
    "/{task_id}",
    response_model=Task,
    responses={
        404: {"description": "Task not found!"},
    },
    operation_id="get_task",
    dependencies=[Depends(JWTBearer())],
)
async def get_task(
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
) -> Task:
    """Get all information about a labelling task"""
    task_folder = SETTINGS.data_folder.joinpath(task_id)
    task_file = task_folder.joinpath("task.json")
    if not (task_folder.exists() and task_file.exists()):
        raise HTTPException(
            status_code=404,
            detail="Task not found!",
        )
    with open(task_file, "r", encoding="utf-8") as file:
        return json.load(file)
