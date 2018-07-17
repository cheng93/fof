from sqlalchemy import (Column, ForeignKey, MetaData, SmallInteger, 
                        String, Table)

metadata = MetaData()


team = Table(
    'team', metadata,
    Column('team_id', SmallInteger, primary_key=True),
    Column('city', String(50), nullable=False),
    Column('team_name', String(50), nullable=False),
    Column('division_id', ForeignKey(
        'division.division_id', onupdate='CASCADE'), nullable=False)
)
