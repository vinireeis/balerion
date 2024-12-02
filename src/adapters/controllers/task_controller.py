from http import HTTPStatus

from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    PatchTaskStatusRequest,
    UpdateTaskRequest,
)
from src.adapters.data_types.responses.tasks_response import (
    DeleteTaskResponse,
    GetOneTaskResponse,
    NewTaskResponse,
    TaskIdPayload,
    TaskPayload,
    TasksPaginatedPayload,
    TasksPaginatedResponse,
    UpdateTaskResponse,
    UpdateTaskStatusResponse,
)
from src.services.tasks.service import TasksService


class TasksController:
    _task_service: TasksService = TasksService()

    @classmethod
    async def create_task(cls, request: NewTaskRequest) -> NewTaskResponse:
        new_user_model = await TasksService.create_new_task(
            request=request,
        )

        response = NewTaskResponse(
            payload=TaskIdPayload(id=new_user_model.id),
            success=True,
            message='Task has been created.',
            status_code=HTTPStatus.CREATED,
        )

        return response

    @classmethod
    async def get_task_by_id(cls, task_id: int) -> GetOneTaskResponse:
        task_model = await TasksService.get_task_by_id(task_id=task_id)
        response = GetOneTaskResponse(
            payload=TaskPayload(
                id=task_model.id,
                title=task_model.title,
                description=task_model.description,
                status=task_model.status,
                priority=task_model.priority,
                deadline=task_model.deadline,
                created_at=task_model.created_at,
                updated_at=task_model.updated_at,
            ),
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def get_tasks_paginated(
        cls,
        limit: int,
        offset: int,
    ) -> TasksPaginatedResponse:
        tasks_result = await TasksService.get_tasks_paginated(
            limit=limit, offset=offset
        )
        tasks_payload_list = [
            TaskPayload(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                priority=task.priority,
                deadline=task.deadline,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks_result.get('tasks', [])
        ]
        response = TasksPaginatedResponse(
            payload=TasksPaginatedPayload(
                tasks=tasks_payload_list,
                total=tasks_result.get('total'),
                limit=tasks_result.get('limit'),
                offset=tasks_result.get('offset'),
            ),
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def update_task(
        cls, update_task_request: UpdateTaskRequest
    ) -> UpdateTaskResponse:
        await TasksService.update_task(request=update_task_request)
        response = UpdateTaskResponse(
            success=True,
            message='Task has been updated.',
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def patch_task_status(
        cls, patch_status_request: PatchTaskStatusRequest
    ) -> UpdateTaskStatusResponse:
        await TasksService.patch_task_status(request=patch_status_request)
        response = UpdateTaskStatusResponse(
            success=True,
            message='Task status has been updated.',
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def delete_task(cls, task_id: int) -> DeleteTaskResponse:
        await TasksService.delete_task(task_id=task_id)
        response = DeleteTaskResponse(
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response
