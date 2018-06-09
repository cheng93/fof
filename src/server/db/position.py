from sqlalchemy import Column, MetaData, String, Table

metadata = MetaData()


position = Table(
    'position', metadata,
    Column('position', String(4), primary_key=True)
)
