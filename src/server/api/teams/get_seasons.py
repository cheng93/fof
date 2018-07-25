import sqlalchemy as sa
from marshmallow import Schema, fields
from api.command import Command
from db.views import team_final_standing, team_season_summary

class GetSeasonsSchema(Schema):
    class Meta:
        fields = ("team_id", "year", "wins", "loses", "ties",
                    "win_lose_percent", "standing_name")

def seasons_query(team_id):
    join = (team_season_summary
        .join(team_final_standing,
            sa.and_(
                team_final_standing.c.team_id == team_season_summary.c.team_id,
                team_final_standing.c.year == team_season_summary.c.year)))
    return (sa.select([
                team_season_summary,
                team_final_standing.c.standing_name
            ])
            .select_from(join)
            .where(team_season_summary.c.team_id == team_id)
            .order_by(team_season_summary.c.year))

class GetSeasonsCommand(Command):
    def __init__(self, db, team_id):
        self.db = db
        self.team_id = team_id

    async def execute(self):
        async with self.db.acquire() as conn:
            cursor = await conn.execute(seasons_query(self.team_id))
            records = await cursor.fetchall()
            schema = GetSeasonsSchema()
            (seasons, errors) = schema.dump(records, many=True)

            return seasons