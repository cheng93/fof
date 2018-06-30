from marshmallow import Schema, fields
from api.command import Command
from db import team

class GetTeamSchema(Schema):
    name = fields.Function(lambda obj: f"{obj.city} {obj.team_name}")
    class Meta:
        fields = ("team_id", "name")

class GetTeamCommand(Command):
    def __init__(self, db, team_id):
        self.db = db
        self.team_id = team_id

    async def execute(self):
        async with self.db.acquire() as conn:
            query = team.select().where(team.c.team_id == self.team_id)
            cursor = await conn.execute(query)
            record = await cursor.first()
            schema = GetTeamSchema()
            (data, errors) = schema.dump(record)
            return data
