from http import HTTPStatus

from flask import Blueprint, jsonify, request

from src.adapters.controllers.task_controller import TasksController
from src.adapters.data_types.requests.tasks_request import NewTaskRequest

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
    def create_task():
        raw_new_task = request.json
        new_task_request = NewTaskRequest(**raw_new_task)
        response = TasksController.create_task(request=new_task_request)

        return response

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
    def get_one_task(task_id: int):
        pass

    @staticmethod
    @tasks_blueprint.route('/tasks', methods=['GET'])
    def get_paginated_tasks():
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        response = TasksController.get_tasks_paginated(
            limit=limit, offset=offset
        )
        return response

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
    def patch_task_status(task_id: int):
        pass

    @staticmethod
    @tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id: int):
        pass
