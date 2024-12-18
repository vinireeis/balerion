from datetime import date, datetime

from pydantic import BaseModel, Field

from src.adapters.data_types.responses.base.base_response import BaseResponse
from src.domain.enums.tasks.enum import TaskPriorityEnum, TaskStatusEnum


class TaskPayload(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatusEnum
    priority: TaskPriorityEnum
    deadline: date | None
    created_at: datetime
    updated_at: datetime


class TasksPaginatedPayload(BaseModel):
    tasks: list[TaskPayload] = Field(default_factory=list)
    total: int
    limit: int
    offset: int


class TaskIdPayload(BaseModel):
    id: int


class TasksPaginatedResponse(BaseResponse):
    payload: TasksPaginatedPayload


class GetOneTaskResponse(BaseResponse):
    payload: TaskPayload


class NewTaskResponse(BaseResponse):
    payload: TaskIdPayload
    status: int = Field(default=201)


class UpdateTaskResponse(BaseResponse):
    pass


class PatchTaskStatusResponse(BaseResponse):
    pass


class DeleteTaskResponse(BaseResponse):
    pass
