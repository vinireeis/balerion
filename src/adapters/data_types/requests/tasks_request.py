from datetime import date
from typing import Annotated

from decouple import config
from pydantic import BaseModel, BeforeValidator, field_validator

from src.adapters.data_types.requests import model_config_example
from src.domain.enums.tasks.enum import TaskPriorityEnum, TaskStatusEnum

UpperStatus = Annotated[
    TaskStatusEnum,
    BeforeValidator(
        lambda task_status: task_status.upper() if task_status else task_status
    ),
]

UpperPriority = Annotated[
    TaskPriorityEnum,
    BeforeValidator(
        lambda task_priority: task_priority.upper()
        if task_priority
        else task_priority
    ),
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

    @classmethod
    def get_swagger_schema(cls):
        schema = cls.model_json_schema()

        schema['definitions'] = schema.pop('$defs')

        for prop in schema['properties'].values():
            if isinstance(prop, dict) and '$ref' in prop:
                prop['$ref'] = prop['$ref'].replace('/$defs/', '/definitions/')

        return schema


class NewTaskRequest(BaseTaskRequest):
    status: UpperStatus = TaskStatusEnum.TODO
    priority: UpperPriority = TaskPriorityEnum.MEDIUM

    model_config = model_config_example


class UpdateTaskRequest(BaseTaskRequest):
    status: UpperStatus = None
    priority: UpperPriority = None
    task_id: int

    model_config = model_config_example


class PatchTaskStatusRequest(BaseModel):
    status: UpperStatus
    task_id: int

    @classmethod
    def get_swagger_schema(cls):
        schema = cls.model_json_schema()

        schema['definitions'] = schema.pop('$defs')

        for prop in schema['properties'].values():
            if isinstance(prop, dict) and '$ref' in prop:
                prop['$ref'] = prop['$ref'].replace('/$defs/', '/definitions/')

        return schema
