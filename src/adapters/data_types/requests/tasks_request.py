from datetime import date
from typing import Annotated

from decouple import config
from pydantic import BaseModel, BeforeValidator, field_validator

from src.domain.enums.tasks.enum import TaskPriorityEnum, TaskStatusEnum

UpperStatus = Annotated[
    TaskStatusEnum, BeforeValidator(lambda x: x.upper() if x else x)
]

UpperPriority = Annotated[
    TaskPriorityEnum, BeforeValidator(lambda x: x.upper() if x else x)
]


class BaseTaskRequest(BaseModel):
    title: str
    description: str | None = None
    deadline: date | None = None

    @field_validator('title')
    def validate_title(cls, title: str) -> str:
        title = title.strip()
        if len(title) > int(config('TITLE_MAX_CHAR')):
            raise ValueError('Title must be 100 characters or less')
        return title

    @field_validator('deadline')
    def validate_deadline(cls, deadline: date | None) -> date | None:
        if deadline and deadline < date.today():
            raise ValueError('Deadline cannot be in the past')
        return deadline


class NewTaskRequest(BaseTaskRequest):
    status: UpperStatus = TaskStatusEnum.TODO
    priority: UpperPriority = TaskPriorityEnum.MEDIUM


class UpdateTaskRequest(BaseTaskRequest):
    status: UpperStatus = None
    priority: UpperPriority = None
    task_id: int


class PatchTaskStatusRequest(BaseModel):
    status: UpperStatus
    task_id: int
