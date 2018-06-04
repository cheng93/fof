import os


def execute(year):
    sql = f'''
        INSERT INTO year (year)
        VALUES ({year})
        ;
    '''

    return sql
