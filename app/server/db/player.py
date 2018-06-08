from sqlalchemy import (Column, Date, ForeignKey, Integer, MetaData, 
                        SmallInteger, String, Table)

metadata = MetaData()


player = Table(
    'player', metadata,
    Column('player_id', Integer, primary_key=True),
    Column('last_name', String(126), nullable=False),
    Column('first_name', String(126), nullable=False),
    Column('position', ForeignKey('position.position',
                                  onupdate='CASCADE'), nullable=False),
    Column('height', SmallInteger, nullable=False),
    Column('weight', SmallInteger, nullable=False),
    Column('birth_date', Date, nullable=False)
)
