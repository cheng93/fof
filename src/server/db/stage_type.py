from sqlalchemy import Column, MetaData, SmallInteger, String, Table

metadata = MetaData()


stage_type = Table(
    'stage_type', metadata,
    Column('stage_type', String(50), primary_key=True),
    Column('rank', SmallInteger, nullable=False, unique=True)
)
