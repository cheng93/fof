import pathlib
from aiohttp import web

routes = web.RouteTableDef()

PROJECT_ROOT = pathlib.Path(__file__).parent

@routes.get("/")
async def index(request):
    return web.FileResponse(f"{PROJECT_ROOT}/index.html")