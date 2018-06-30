from sqlalchemy import Column, MetaData, Numeric, SmallInteger, String, Table

metadata = MetaData()


team_overall_summary = Table(
    'team_overall_summary', metadata,
    Column('team_id', SmallInteger),
    Column('wins', SmallInteger),
    Column('loses', SmallInteger),
    Column('ties', SmallInteger),
    Column('win_lose_percent', Numeric),
    Column('conference_wins', SmallInteger),
    Column('superbowl_wins', SmallInteger),
    Column('playoff_appearances', SmallInteger)

)

