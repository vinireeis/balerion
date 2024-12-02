from http import HTTPStatus

from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import RepositoryException


class TaskNotFoundError(RepositoryException):
    def __init__(self, task_id, *args, **kwargs):
        self.msg = f'Task with ID {task_id} not found.'
        self.status_code = HTTPStatus.NOT_FOUND
        self.internal_code = InternalCodeEnum.DATA_NOT_FOUND
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )


class TaskAlreadyInStatusError(RepositoryException):
    def __init__(self, task_id, status, *args, **kwargs):
        self.msg = f'Task {task_id} is already in {status} status'
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCodeEnum.STATUS_TRANSITION_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )


class UnexpectedRepositoryError(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = (
            'An unexpected error occurred while trying to use the repository.'
        )
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCodeEnum.INTERNAL_SERVER_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )
