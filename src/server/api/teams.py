from aiohttp import web
from db import team

routes = web.RouteTableDef()

@routes.get('/teams/')
async def get_teams(request):
    async with request.app["db"].acquire() as conn:
        query = team.select().order_by(team.c.city)
        cursor = await conn.execute(query)
        records = await cursor.fetchall()
        teams = [dict(t) for t in records]
        return web.json_response({'teams': teams})
