from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    UpdateTaskRequest,
    UpdateTaskStatusRequest,
)
from src.adapters.data_types.typed_dicts.tasks_typed_dict import (
    PaginatedTasksTypedDict,
)
from src.adapters.repositories.tasks.repository import TaskRepository
from src.domain.models.tasks.model import TaskModel


class TasksService:
    _task_repository: TaskRepository = TaskRepository()

    @classmethod
    async def create_new_task(cls, request: NewTaskRequest) -> TaskModel:
        new_task_model = await cls._task_repository.insert_one_task(
            task_request=request
        )

        return new_task_model

    @classmethod
    async def get_tasks_paginated(
        cls,
        limit: int,
        offset: int,
    ) -> PaginatedTasksTypedDict:
        tasks_paginated_result = (
            await cls._task_repository.get_tasks_paginated(
                limit=limit, offset=offset
            )
        )

        return tasks_paginated_result

    @classmethod
    async def get_task_by_id(cls, task_id: int) -> TaskModel:
        task_model = await cls._task_repository.get_one_task_by_id(
            task_id=task_id
        )

        return task_model

    @classmethod
    async def update_task(
        cls,
        task_id: int,
        request: UpdateTaskRequest,
    ):
        await cls._task_repository.update_task(
            task_id=task_id, task_request=request
        )

    @classmethod
    async def update_task_status(
        cls,
        task_id: int,
        request: UpdateTaskStatusRequest,
    ):
        await cls._task_repository.update_task_status(
            task_id=task_id, new_status=request.status
        )

    @classmethod
    async def delete_task(
        cls,
        task_id: int,
    ):
        await cls._task_repository.delete_one_task_by_id(task_id=task_id)
