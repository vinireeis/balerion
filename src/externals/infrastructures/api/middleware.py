from http import HTTPStatus
from time import time

from flask import Flask, Response, g, jsonify, request
from loguru import logger
from pydantic import ValidationError

from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import (
    RepositoryException,
    ServiceException,
)


class Middleware:
    @staticmethod
    def response_handler(app: Flask):
        @app.before_request
        def before_request():
            g.start_time = time()
            logger.info({
                'method': request.method,
                'path': request.path,
                'body': request.get_data(as_text=True),
            })
            request.start_time = time()

        @app.after_request
        def after_request(response: Response):
            process_time = time() - g.start_time
            response.headers['X-Process-Time'] = str(process_time)
            logger.info({'http_status': response.status_code})
            print(process_time)
            return response

        @app.errorhandler(Exception)
        def handle_exception(error):
            if isinstance(error, RepositoryException):
                logger.info(error.msg)
                return jsonify({
                    'success': False,
                    'message': error.msg,
                    'internal_code': error.internal_code,
                }), error.status_code

            if isinstance(error, ServiceException):
                logger.info(error.msg)
                return jsonify({
                    'success': False,
                    'message': error.msg,
                    'internal_code': error.internal_code,
                }), error.status_code

            if isinstance(error, ValidationError):
                logger.info(error)
                return jsonify({
                    'success': False,
                    'internal_code': InternalCodeEnum.DATA_VALIDATION_ERROR,
                    'message': str(error),
                }), HTTPStatus.INTERNAL_SERVER_ERROR

            logger.info(error)
            return jsonify({
                'success': False,
                'internal_code': InternalCodeEnum.INTERNAL_SERVER_ERROR,
                'message': 'Unexpected error has occurred',
            }), HTTPStatus.INTERNAL_SERVER_ERROR
