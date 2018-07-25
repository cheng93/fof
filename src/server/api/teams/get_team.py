import sqlalchemy as sa
from marshmallow import Schema, fields
from api.command import Command
from db import division, team
from db.views import team_overall_summary

class GetTeamSchema(Schema):
    name = fields.Function(lambda obj: f"{obj.city} {obj.team_name}")
    class Meta:
        fields = ("team_id", "name", "wins", "loses", "ties",
                    "win_lose_percent", "conference_wins",
                    "superbowl_wins", "playoff_appearances",
                    "division")

def team_query(team_id):
    join = (team
        .join(team_overall_summary,
            team_overall_summary.c.team_id == team.c.team_id)
        .join(division,
            division.c.division_id == team.c.division_id))
    return (sa.select([
                team_overall_summary,
                team.c.team_name,
                team.c.city,
                division.c.name.label("division")
            ])
            .select_from(join)
            .where(team.c.team_id == team_id))

class GetTeamCommand(Command):
    def __init__(self, db, team_id):
        self.db = db
        self.team_id = team_id

    async def execute(self):
        async with self.db.acquire() as conn:
            cursor = await conn.execute(team_query(self.team_id))
            record = await cursor.first()
            schema = GetTeamSchema()
            (t, errors) = schema.dump(record)

            return t
