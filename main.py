import asyncio

from asgiref.wsgi import WsgiToAsgi
from decouple import config as decouple_environment
from hypercorn.asyncio import serve
from pyfiglet import print_figlet

from src.externals.infrastructures.api.infrastructure import ApiInfrastructure

app = ApiInfrastructure.get_app()
asgi_app = WsgiToAsgi(app)

hypercorn_config = ApiInfrastructure.get_hypercorn_config()


if __name__ == '__main__':
    host = decouple_environment('HOST', default='0.0.0.0')
    port = decouple_environment('PORT', default=5000, cast=int)
    hypercorn_config.bind = [f'{host}:{port}']
    print_figlet(text='balerion-api', colors='0;78;225', width=200)
    print(f'Server is ready at URL {host}:{port}')
    asyncio.run(serve(asgi_app, hypercorn_config))
