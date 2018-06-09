from sqlalchemy import (CheckConstraint, Column, Float, ForeignKey,
                        Integer, MetaData, SmallInteger, String, 
                        Table, text)

metadata = MetaData()


game = Table(
    'game', metadata,
    Column('game_id', Integer, primary_key=True, server_default=text(
        "nextval('game_game_id_seq'::regclass)")),
    Column('year', ForeignKey('year.year'), nullable=False),
    Column('stage_id', ForeignKey('stage.stage_id'), nullable=False),
    Column('home_team_id', ForeignKey(
        'team.team_id', onupdate='CASCADE'), nullable=False),
    Column('home_score', SmallInteger, nullable=False),
    Column('visitor_team_id', ForeignKey(
        'team.team_id', onupdate='CASCADE'), nullable=False),
    Column('visitor_score', SmallInteger, nullable=False),
    Column('attendance', Integer),
    Column('weather', String(50)),
    Column('wind', Float),
    Column('temperature', Float),
    CheckConstraint('home_team_id <> visitor_team_id')
)
