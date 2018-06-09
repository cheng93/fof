from sqlalchemy import Column, Integer, MetaData, SmallInteger, Table
                        

metadata = MetaData()


player_latest_team = Table(
    'player_latest_team', metadata,
    Column('player_id', Integer),
    Column('team_id', SmallInteger)
)
