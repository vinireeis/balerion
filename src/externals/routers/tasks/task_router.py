from http import HTTPStatus

from flask import Blueprint, jsonify, request

from src.adapters.controllers.task_controller import TasksController
from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    PatchTaskStatusRequest,
    UpdateTaskRequest,
)

tasks_blueprint = Blueprint(name='tasks', import_name=__name__)


class TasksRouter:
    @staticmethod
    @tasks_blueprint.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'api-status': 'BalerionAPI ready',
            'service': 'balerion-api',
            'version': '0.1.0',
        }), HTTPStatus.OK

    @staticmethod
    @tasks_blueprint.route('/tasks', methods=['POST'])
    async def create_task():
        raw_new_task = request.json
        new_task_request = NewTaskRequest(**raw_new_task)
        response = await TasksController.create_task(request=new_task_request)

        return jsonify(response.model_dump(), HTTPStatus.CREATED)

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
    async def get_one_task(task_id: int):
        response = await TasksController.get_task_by_id(task_id=task_id)
        return jsonify(response.model_dump(), HTTPStatus.OK)

    @staticmethod
    @tasks_blueprint.route('/tasks', methods=['GET'])
    async def get_paginated_tasks():
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        response = await TasksController.get_tasks_paginated(
            limit=limit, offset=offset
        )
        return jsonify(response.model_dump(), HTTPStatus.OK)

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
    async def update_task(task_id: int):
        raw_update_task = request.json
        update_task_request = UpdateTaskRequest(
            **raw_update_task, task_id=task_id
        )
        response = await TasksController.update_task(
            update_task_request=update_task_request
        )
        return jsonify(response.model_dump(), HTTPStatus.OK)

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['PATCH'])
    async def patch_task_status(task_id: int):
        raw_patch_status = request.json
        patch_task_status_request = PatchTaskStatusRequest(
            task_id=task_id,
            status=raw_patch_status.get('status'),
        )
        response = await TasksController.patch_task_status(
            patch_status_request=patch_task_status_request
        )
        return jsonify(response.model_dump(), HTTPStatus.OK)

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
    async def delete_task(task_id: int):
        response = await TasksController.delete_task(task_id=task_id)
        return jsonify(response.model_dump(), HTTPStatus.OK)