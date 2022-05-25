"""Routes for tasks"""

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from mod.src.models.task import TaskType

from mod.src.auth.auth_bearer import JWTBearer
from mod.src.models.task import BaseTask, SpecificTask, TaskNotFoundException
from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

class TaskTypeGuard:
    """Guard for task types"""

    def __init__(self, task_type: TaskType):
        self.task_type = task_type

    async def __call__(self, request: Request) -> None:
        """Check if the task type is correct"""
        task_id = request.path_params["task_id"]
        print(task_id)
        task_file = SETTINGS.data_folder.joinpath(task_id).joinpath("task.json")
        task = BaseTask.load_from_file(task_file)
        if task.type_id != self.task_type:
            raise HTTPException(status_code=403, detail="Invalid task type")

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
