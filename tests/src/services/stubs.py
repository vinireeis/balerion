from datetime import date

from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    PatchTaskStatusRequest,
    UpdateTaskRequest,
)
from src.domain.enums.tasks.enum import TaskPriorityEnum, TaskStatusEnum
from src.domain.models.tasks.model import TaskModel

task_model_stub = TaskModel(
    id=1,
    title='Test Task',
    description='Test description',
    status=TaskStatusEnum.TODO,
    priority=TaskPriorityEnum.HIGH,
    deadline=date.fromisoformat('2024-12-31'),
)

new_task_request_stub = NewTaskRequest(
    title='New Task',
    description='New task description',
    status=TaskStatusEnum.TODO,
    priority=TaskPriorityEnum.MEDIUM,
    deadline=date.fromisoformat('2024-12-31'),
)

update_task_request_stub = UpdateTaskRequest(
    task_id=1,
    title='Updated Task',
    description='Updated description',
    status=TaskStatusEnum.DOING,
    priority=TaskPriorityEnum.LOW,
    deadline=date.fromisoformat('2024-12-15'),
)

patch_task_status_request_stub = PatchTaskStatusRequest(
    task_id=1, status=TaskStatusEnum.DONE
)

paginated_tasks_stub = {
    'tasks': [task_model_stub],
    'total': 1,
    'limit': 10,
    'offset': 0,
}
