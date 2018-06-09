from sqlalchemy import (Column, ForeignKey, Integer, MetaData,
                        SmallInteger, String, Table)

metadata = MetaData()


staff = Table(
    'staff', metadata,
    Column('staff_id', Integer, primary_key=True),
    Column('last_name', String(126), nullable=False),
    Column('first_name', String(126), nullable=False),
    Column('birth_year', SmallInteger, nullable=False),
    Column('staff_group', ForeignKey('staff_group.staff_group'), nullable=False)
)
