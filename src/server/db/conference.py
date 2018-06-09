from sqlalchemy import Column, MetaData, SmallInteger, String, Table

metadata = MetaData()


conference = Table(
    'conference', metadata,
    Column('conference_id', SmallInteger, primary_key=True),
    Column('name', String(50), nullable=False)
)
