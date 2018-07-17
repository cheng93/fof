from sqlalchemy import Column, MetaData, String, Table

metadata = MetaData()


staff_role = Table(
    'staff_role', metadata,
    Column('staff_role', String(50), primary_key=True)
)
