from typing import TypedDict

from src.domain.models.tasks.model import TaskModel


class PaginatedTasksTypedDict(TypedDict):
    tasks: list[TaskModel]
    total: int
    limit: int
    offset: int
