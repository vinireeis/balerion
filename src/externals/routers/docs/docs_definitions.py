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
    PatchTaskStatusResponse,
    TasksPaginatedResponse,
    UpdateTaskResponse,
)

map_doc_definitions = {
    'health_check': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'task_id',
                'in': 'path',
                'type': 'integer',
                'required': 'true',
                'description': 'Task ID',
            }
        ],
        'responses': {
            HTTPStatus.OK: {
                'description': 'Task details',
                'schema': GetOneTaskResponse.get_swagger_schema(),
            }
        },
    },
    'new_task': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': 'true',
                'schema': NewTaskRequest.get_swagger_schema(),
            }
        ],
        'responses': {
            HTTPStatus.CREATED: {
                'description': 'Todo list',
                'schema': NewTaskResponse.get_swagger_schema(),
            }
        },
    },
    'one_task': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'task_id',
                'in': 'path',
                'type': 'integer',
                'required': 'true',
                'description': 'Task ID',
            }
        ],
        'responses': {
            HTTPStatus.OK: {
                'description': 'Task details',
                'schema': GetOneTaskResponse.get_swagger_schema(),
            }
        },
    },
    'paginated_tasks': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'limit',
                'in': 'query',
                'type': 'integer',
                'required': 'false',
                'default': 10,
            },
            {
                'name': 'offset',
                'in': 'query',
                'type': 'integer',
                'required': 'false',
                'default': 0,
            },
        ],
        'responses': {
            HTTPStatus.OK: {
                'description': 'List of tasks',
                'schema': TasksPaginatedResponse.get_swagger_schema(),
            }
        },
    },
    'update_one_task': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'task_id',
                'in': 'path',
                'type': 'integer',
                'required': 'true',
                'description': 'Task ID',
            },
            {
                'name': 'body',
                'in': 'body',
                'required': 'true',
                'schema': UpdateTaskRequest.get_swagger_schema(),
            },
        ],
        'responses': {
            HTTPStatus.OK: {
                'description': 'Task updated',
                'schema': UpdateTaskResponse.get_swagger_schema(),
            }
        },
    },
    'patch_task_status': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'task_id',
                'in': 'path',
                'type': 'integer',
                'required': 'true',
                'description': 'Task ID',
            },
            {
                'name': 'body',
                'in': 'body',
                'required': 'true',
                'schema': PatchTaskStatusRequest.get_swagger_schema(),
            },
        ],
        'responses': {
            HTTPStatus.OK: {
                'description': 'Task status updated',
                'schema': PatchTaskStatusResponse.get_swagger_schema(),
            }
        },
    },
    'delete_one_task': {
        'tags': ['Tasks'],
        'parameters': [
            {
                'name': 'task_id',
                'in': 'path',
                'type': 'integer',
                'required': 'true',
                'description': 'Task ID',
            }
        ],
        'responses': {
            HTTPStatus.OK: {
                'description': 'Task deleted',
                'schema': DeleteTaskResponse.get_swagger_schema(),
            }
        },
    },
}
