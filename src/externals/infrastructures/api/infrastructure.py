import logging

from decouple import config as decouple_environment
from flasgger import Swagger
from flask import Flask
from hypercorn import Config

from src.externals.infrastructures.api.middleware import Middleware
from src.externals.routers.tasks.task_router import tasks_blueprint

logging.basicConfig(level=logging.DEBUG)

swagger_template = {
    'swagger': '2.0',
    'info': {
        'title': 'Balerion API',
        'description': 'Task Management API Documentation',
        'version': '1.0.0',
    },
}


class ApiInfrastructure:
    app: Flask = None
    swagger: Swagger = None

    @classmethod
    def get_app(cls) -> Flask:
        if cls.app is None:
            cls.app = Flask(__name__)
            cls.swagger = Swagger(app=cls.app, template=swagger_template)

        cls._configure_app()
        return cls.app

    @classmethod
    def _configure_app(cls) -> None:
        cls._set_api_config()
        cls._register_routers()
        Middleware.response_handler(app=cls.app)

    @classmethod
    def _set_api_config(cls):
        cls.app.config['API_TITLE'] = 'ToDoList API'
        cls.app.config['API_VERSION'] = 'v1'
        cls.app.debug = True

    @classmethod
    def _register_routers(cls):
        cls.app.register_blueprint(tasks_blueprint)

    @staticmethod
    def get_hypercorn_config() -> Config:
        host = decouple_environment('HOST', default='0.0.0.0')
        port = decouple_environment('PORT', default=5000, cast=int)
        config = Config()
        config.use_reloader = True
        config.access_log = True
        config.bind = [f'{host}:{port}']
        return config
