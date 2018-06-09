import pathlib
from views import routes

PROJECT_ROOT = pathlib.Path(__file__).parent

def setup_routes(app):
    app.router.add_routes(routes)
    app.router.add_static("/static/", path=f"{PROJECT_ROOT}/static")