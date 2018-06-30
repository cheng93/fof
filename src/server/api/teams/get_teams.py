import sqlalchemy as sa
from marshmallow import Schema, fields
from api.command import Command
from db import team
from db.views import team_overall_summary

class GetTeamsSchema(Schema):
    name = fields.Function(lambda obj: f"{obj.city} {obj.team_name}")
    class Meta:
        fields = ("team_id", "name", "wins", "loses", "ties",
                    "win_lose_percent", "conference_wins",
                    "superbowl_wins", "playoff_appearances")

class GetTeamsCommand(Command):
    def __init__(self, db):
        self.db = db

    async def execute(self):
        async with self.db.acquire() as conn:
            join = team_overall_summary.join(team, 
                team.c.team_id == team_overall_summary.c.team_id)
            query = (sa.select([
                        team_overall_summary,
                        team.c.team_name, 
                        team.c.city
                    ])
                    .select_from(join)
                    .order_by(team.c.city))
            cursor = await conn.execute(query)
            records = await cursor.fetchall()
            schema = GetTeamsSchema()
            (data, errors) = schema.dump(records, many=True)
            return data
