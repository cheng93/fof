from aiohttp import web
from api.pg import close_pg, init_pg
from api.routes import setup_routes

app = web.Application()

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

setup_routes(app)
