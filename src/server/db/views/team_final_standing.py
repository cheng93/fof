from sqlalchemy import Column, MetaData, SmallInteger, Table, Text

metadata = MetaData()


team_final_standing = Table(
    'team_final_standing', metadata,
    Column('team_id', SmallInteger),
    Column('year', SmallInteger),
    Column('standing_name', Text)
)
