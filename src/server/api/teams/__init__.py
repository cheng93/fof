import simplejson
from aiohttp import web
from api.command import CommandRunnerMixin
from api.teams.get_seasons import GetSeasonsCommand
from api.teams.get_team import GetTeamCommand
from api.teams.get_teams import GetTeamsCommand

routes = web.RouteTableDef()

@routes.view("/teams/")
class TeamsView(web.View, CommandRunnerMixin):
    async def get(self):
        command = GetTeamsCommand(self.request.app["db"])
        data = await self.execute(command)
        json = simplejson.dumps({"teams": data})
        return web.json_response(text=json)

@routes.view("/teams/{team_id}")
class TeamView(web.View, CommandRunnerMixin):
    async def get(self):
        db = self.request.app["db"]
        team_id = self.request.match_info["team_id"]
        command = GetTeamCommand(db, team_id)
        data = await self.execute(command)
        json = simplejson.dumps(data)
        return web.json_response(text=json)

@routes.view("/teams/{team_id}/seasons")
class TeamSeasonsView(web.View, CommandRunnerMixin):
    async def get(self):
        db = self.request.app["db"]
        team_id = self.request.match_info["team_id"]
        command = GetSeasonsCommand(db, team_id)
        data = await self.execute(command)
        json = simplejson.dumps({"seasons": data})
        return web.json_response(text=json)