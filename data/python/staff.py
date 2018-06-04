from base_fof import BaseFof
import csv
import os


class Staff(BaseFof):
    def execute(self, cursor, year, start_id):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            df["Year"] = int(year)
            df = df.query(f"Staff_ID >= {int(start_id)}")
            return df

        file_name="staff.csv"

        table_name = "temp_staff"
        table_definition = """
            temp_staff_id SERIAL PRIMARY KEY,
            staff_id INTEGER,
            last_name VARCHAR(126),
            first_name VARCHAR(126),
            year SMALLINT,
            age SMALLINT,
            primary_group VARCHAR(50)
        """

        columns=[
            "Staff_ID",
            "Last_Name",
            "First_Name",
            "Year",
            "Age",
            "Primary_Group"
        ]

        migrate_sql = f"""
            INSERT INTO staff
            (
                staff_id,
                last_name,
                first_name,
                birth_year,
                staff_group
            )
            SELECT
                t.staff_id,
                t.last_name,
                t.first_name,
                t.year - t.age,
                t.primary_group
            FROM {table_name} t
        """

        super().execute(
            cursor=cursor,
            year=year,
            file_name=file_name,
            manipulate_df=manipulate_df,
            table_name=table_name,
            table_definition=table_definition,
            columns=columns,
            migrate_sql=migrate_sql)
