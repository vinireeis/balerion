import pytest

from src.domain.models.tasks.model import TaskModel
from src.services.tasks.service import TasksService
from tests.src.services.stubs import (
    new_task_request_stub,
    patch_task_status_request_stub,
    task_model_stub,
    update_task_request_stub,
)


@pytest.mark.asyncio
async def test_when_get_task_by_id_then_return_task(mock_task_repository):
    task = await TasksService.get_task_by_id(task_id=1)

    mock_task_repository.get_one_task_by_id.assert_called_once_with(task_id=1)
    assert task.id == 1
    assert task.title == 'Test Task'


@pytest.mark.asyncio
async def test_when_get_tasks_paginated_then_return_tasks(
    mock_task_repository,
):
    tasks = await TasksService.get_tasks_paginated(limit=10, offset=0)

    mock_task_repository.get_tasks_paginated.assert_called_once_with(
        limit=10, offset=0
    )
    assert len(tasks['tasks']) == 1
    assert tasks['tasks'][0].title == 'Test Task'


@pytest.mark.asyncio
async def test_when_create_new_task_then_return_task_model(
    mock_task_repository,
):
    new_task = await TasksService.create_new_task(
        request=new_task_request_stub
    )

    mock_task_repository.insert_one_task.assert_called_once_with(
        task_request=new_task_request_stub
    )
    assert isinstance(new_task, TaskModel)
    assert new_task == task_model_stub


@pytest.mark.asyncio
async def test_when_update_task_then_repository_is_called(
    mock_task_repository,
):
    await TasksService.update_task(request=update_task_request_stub)

    mock_task_repository.update_task.assert_called_once_with(
        task_id=update_task_request_stub.task_id,
        task_request=update_task_request_stub,
    )


@pytest.mark.asyncio
async def test_when_patch_task_status_then_repository_is_called(
    mock_task_repository,
):
    await TasksService.patch_task_status(
        request=patch_task_status_request_stub
    )

    mock_task_repository.update_task_status.assert_called_once_with(
        request=patch_task_status_request_stub
    )


@pytest.mark.asyncio
async def test_when_delete_task_then_repository_is_called(
    mock_task_repository,
):
    await TasksService.delete_task(task_id=1)

    mock_task_repository.delete_one_task_by_id.assert_called_once_with(
        task_id=1
    )
