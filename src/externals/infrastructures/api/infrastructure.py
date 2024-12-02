import logging

from decouple import config as decouple_environment
from flask import Flask
from hypercorn import Config

from src.externals.infrastructures.api.middleware import Middleware
from src.externals.routers.tasks.task_router import tasks_blueprint

logging.basicConfig(level=logging.DEBUG)


class ApiInfrastructure:
    app: Flask = None

    @classmethod
    def get_app(cls):
        if cls.app is None:
            cls.app = Flask(__name__)

        cls.set_api_config()
        cls.register_routers()
        Middleware.response_handler(app=cls.app)

        return cls.app

    @classmethod
    def set_api_config(cls):
        cls.app.config['API_TITLE'] = 'Todo API'
        cls.app.config['API_VERSION'] = 'v1'
        cls.app.config['APPLICATION_ROOT'] = '/balerion-api/v1'
        cls.app.debug = True

    @classmethod
    def register_routers(cls):
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
