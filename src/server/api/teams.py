import simplejson
from aiohttp import web
from marshmallow import Schema, fields
from db.views import team_overall_summary

routes = web.RouteTableDef()

@routes.view('/teams/')
class TeamsView(web.View):
    class GetTeamsSchema(Schema):
        name = fields.Function(lambda obj: f"{obj.city} {obj.team_name}")
        class Meta:
            fields = ("team_id", "name", "wins", "loses", "ties",
                        "win_lose_percent", "conference_wins",
                        "superbowl_wins", "playoff_appearances")

    async def get(self):
        async with self.request.app["db"].acquire() as conn:
            query = (team_overall_summary
                .select()
                .order_by(team_overall_summary.c.city))
            cursor = await conn.execute(query)
            records = await cursor.fetchall()
            schema = TeamsView.GetTeamsSchema()
            (data, errors) = schema.dump(records, many=True)
            json = simplejson.dumps({'teams': data})
            return web.json_response(text=json)
