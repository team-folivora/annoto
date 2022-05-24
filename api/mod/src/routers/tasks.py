"""Routes for tasks"""

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from mod.src.models.task import TaskNotFoundException
from mod.src.models.task import SpecificTask

from mod.src.auth.auth_bearer import JWTBearer
from mod.src.models.task import BaseTask
from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@ROUTER.get(
    "/",
    response_model=List[BaseTask],
    operation_id="get_tasks",
    dependencies=[Depends(JWTBearer())],
)
async def get_tasks() -> List[BaseTask]:
    """Get a list of all available labeling tasks"""
    tasks_file = SETTINGS.data_folder.joinpath("tasks.json")
    tasks = []
    task_ids = []
    with open(tasks_file, "r", encoding="utf-8") as file:
        task_ids = json.load(file)
    for task_id in task_ids:
        task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
        tasks.append(BaseTask.load_from_file(task_file))
    return tasks


@ROUTER.get(
    "/{task_id}",
    response_model=SpecificTask,
    responses={
        404: {"description": "Task not found!"},
    },
    operation_id="get_task",
    dependencies=[Depends(JWTBearer())],
)
async def get_task(
    task_id: str = Path(..., example="ecg-qrs-classification-physiodb"),
) -> SpecificTask:
    """Get all information about a labelling task"""
    task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
    try:
        return BaseTask.load_from_file(task_file)
    except TaskNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Task not found!",
        )
