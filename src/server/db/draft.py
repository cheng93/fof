from sqlalchemy import (Column, ForeignKey, MetaData, SmallInteger,
                        Table)

metadata = MetaData()


draft = Table(
    'draft', metadata,
    Column('year', ForeignKey('year.year'), primary_key=True, nullable=False),
    Column('round', SmallInteger, primary_key=True, nullable=False),
    Column('pick', SmallInteger, primary_key=True, nullable=False),
    Column('player_id', ForeignKey('player.player_id'), nullable=False),
    Column('team_id', ForeignKey('team.team_id'), nullable=False)
)
