from sqlalchemy import Column, MetaData, SmallInteger, Table

metadata = MetaData()


year = Table(
    'year', metadata,
    Column('year', SmallInteger, primary_key=True)
)
