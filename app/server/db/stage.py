from sqlalchemy import (Column, ForeignKey, MetaData, SmallInteger,
                        String, Table, text, UniqueConstraint)

metadata = MetaData()


stage = Table(
    'stage', metadata,
    Column('stage_id', SmallInteger, primary_key=True,
           server_default=text("nextval('stage_stage_id_seq'::regclass)")),
    Column('stage_name', String(50), nullable=False),
    Column('stage_type', ForeignKey('stage_type.stage_type',
                                    onupdate='CASCADE'), nullable=False),
    Column('rank', SmallInteger, nullable=False),
    UniqueConstraint('stage_type', 'rank')
)
