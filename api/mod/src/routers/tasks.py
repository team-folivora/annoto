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
    response_model=List[Task],
    operation_id="get_tasks",
    dependencies=[Depends(JWTBearer())],
)
async def get_tasks() -> List[Task]:
    """Get a list of all available labeling tasks"""
    tasks_file = SETTINGS.data_folder.joinpath("tasks.json")
    tasks = []
    task_ids = []
    if not tasks_file.exists():
        raise HTTPException(status_code=500, detail="Tasks integrity violated")
    with open(tasks_file, "r", encoding="utf-8") as file:
        task_ids = json.load(file)
    for task_id in task_ids:
        task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
        if not task_file.exists():
            raise HTTPException(status_code=500, detail="Tasks integrity violated")
        with open(
            SETTINGS.data_folder.joinpath(task_id).joinpath("task.json"),
            "r",
            encoding="utf-8",
        ) as file:
            tasks.append(Task(**json.load(file)))
    return tasks


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
