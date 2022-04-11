"""Routes for tasks"""

import json
from typing import List

from fastapi import APIRouter

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
)
async def get_tasks() -> List[str]:
    """Get a list of the IDs of all available labelling tasks"""
    tasks_file = SETTINGS.data_folder.joinpath("tasks.json")
    with open(tasks_file, encoding="utf-8") as file:
        return json.load(file)


@ROUTER.get(
    "/{task_id}",
    response_model=Task,
    operation_id="get_task",
)
async def get_task(task_id: str) -> Task:
    """Get all information about a labelling task"""
    task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
    with open(task_file, encoding="uft-8") as file:
        return json.load(file)
