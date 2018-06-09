from sqlalchemy import (Column, ForeignKey, MetaData, SmallInteger,
                        Table)

metadata = MetaData()


staff_history = Table(
    'staff_history', metadata,
    Column('staff_id', ForeignKey('staff.staff_id'),
           primary_key=True, nullable=False),
    Column('year', ForeignKey('year.year'), primary_key=True, nullable=False),
    Column('team_id', ForeignKey('team.team_id'), nullable=False),
    Column('staff_role', ForeignKey('staff_role.staff_role'), nullable=False),
    Column('wins', SmallInteger, nullable=False),
    Column('losses', SmallInteger, nullable=False),
    Column('ties', SmallInteger, nullable=False)
)
