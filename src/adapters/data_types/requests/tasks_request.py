from datetime import date

from decouple import config
from pydantic import BaseModel, field_validator

from src.domain.enums.tasks.enum import TaskPriorityEnum, TaskStatusEnum


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
    status: TaskStatusEnum = TaskStatusEnum.TODO
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM


class UpdateTaskRequest(BaseTaskRequest):
    status: TaskStatusEnum = None
    priority: TaskPriorityEnum = None


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatusEnum
