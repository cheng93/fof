from sqlalchemy import (Column, ForeignKey, MetaData, SmallInteger,
                        String, Table)

metadata = MetaData()


division = Table(
    'division', metadata,
    Column('division_id', SmallInteger, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('conference_id', ForeignKey(
        'conference.conference_id', onupdate='CASCADE'), nullable=False)
)
