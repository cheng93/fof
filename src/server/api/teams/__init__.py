import simplejson
from aiohttp import web
from api.command import CommandRunnerMixin
from api.teams.get_teams import GetTeamsCommand

routes = web.RouteTableDef()

@routes.view('/teams/')
class TeamsView(web.View, CommandRunnerMixin):
    async def get(self):
        command = GetTeamsCommand(self.request.app["db"])
        data = await self.execute(command)
        json = simplejson.dumps({'teams': data})
        return web.json_response(text=json)