from sqlalchemy import Column, MetaData, String, Table

metadata = MetaData()


staff_group = Table(
    'staff_group', metadata,
    Column('staff_group', String(50), primary_key=True)
)
