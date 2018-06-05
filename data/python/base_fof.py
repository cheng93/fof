import io
import pandas
import os
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f"{method.__name__}, {(te - ts) * 1000}")
        return result

    return timed

class BaseFof:
    @timeit
    def get_dataframe(self, year, file_name, **kwargs):
        usecols = kwargs.get("usecols", None)
        dir = os.path.dirname(__file__)
        csvname = os.path.join(dir, f"../{year}/{file_name}")
        df = pandas.read_csv(csvname, encoding="Windows-1252", usecols=usecols)
        return df

    @timeit
    def create_temp_table(self, cursor, table_name, table_definition):
        cursor.execute(f"""
            CREATE TEMP TABLE {table_name} ({table_definition})
            ;
        """)

    @timeit
    def insert_dataframe(self, cursor, df, columns, table):
        buffer = io.StringIO()
        df.to_csv(buffer, header=False, index=False, columns=columns)
        buffer.seek(0)
        cursor.copy_from(buffer, table, sep=",", columns=iter(columns), null="NULL")

    @timeit
    def temp_to_real(self, cursor, sql, table):
        cursor.execute(sql)
        cursor.execute(f"DROP TABLE {table};")

    @timeit
    def manipulate_df_wrapper(self, manipulate_df, df, year):
        return manipulate_df(df, year=year)

    def execute(self, cursor, year, file_name, manipulate_df, 
                      table_name, table_definition, columns, migrate_sql,
                      **kwargs):
        print(self.__class__)
        usecols = kwargs.get("usecols", None)
        df = self.get_dataframe(year, file_name, usecols=usecols)
        df = self.manipulate_df_wrapper(manipulate_df, df, year=year)

        self.create_temp_table(cursor, table_name, table_definition)

        self.insert_dataframe(cursor, df, columns, table_name)

        self.temp_to_real(cursor, migrate_sql, table_name)