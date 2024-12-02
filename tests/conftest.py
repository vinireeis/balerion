from unittest.mock import AsyncMock, patch

import pytest

from tests.src.services.stubs import paginated_tasks_stub, task_model_stub


@pytest.fixture
def mock_task_repository():
    with patch(
        'src.services.tasks.service.TasksService._task_repository'
    ) as mock_task_repo:
        mock_task_repo.insert_one_task = AsyncMock(
            return_value=task_model_stub
        )
        mock_task_repo.get_tasks_paginated = AsyncMock(
            return_value=paginated_tasks_stub
        )
        mock_task_repo.get_one_task_by_id = AsyncMock(
            return_value=task_model_stub
        )
        mock_task_repo.update_task = AsyncMock()
        mock_task_repo.update_task_status = AsyncMock()
        mock_task_repo.delete_one_task_by_id = AsyncMock()
        yield mock_task_repo
