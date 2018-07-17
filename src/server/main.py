from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from routes import setup_routes

from api import app as api_app

app = web.Application(middlewares=[
    normalize_path_middleware()
])

app.add_subapp("/api/", api_app)

setup_routes(app)

web.run_app(app)
