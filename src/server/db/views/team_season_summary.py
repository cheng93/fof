from sqlalchemy import Column, MetaData, Numeric, SmallInteger, Table

metadata = MetaData()


team_season_summary = Table(
    'team_season_summary', metadata,
    Column('team_id', SmallInteger),
    Column('year', SmallInteger),
    Column('wins', SmallInteger),
    Column('loses', SmallInteger),
    Column('ties', SmallInteger),
    Column('win_lose_percent', Numeric)
)
