from base_fof import BaseFof
import csv
import os

class StaffHistory(BaseFof):
    def execute(self, cursor, year):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            df["Year"] = df.apply(lambda x: int(x["Year"])+1, axis=1)
            df = df.query(f"Year == {year}")
            return df

        file_name = "staff_history.csv"

        table_name = "temp_staff_history"
        table_definition = """
            temp_staff_history_id SERIAL PRIMARY KEY,
            staff_id INTEGER,
            year SMALLINT,
            team SMALLINT,
            role VARCHAR(50),
            wins SMALLINT,
            losses SMALLINT,
            ties SMALLINT
        """

        columns=[
            "Staff_ID",
            "Year",
            "Team",
            "Role",
            "Wins",
            "Losses",
            "Ties"
        ]

        migrate_sql = f"""
            INSERT INTO staff_history
            (
                staff_id,
                year,
                team_id,
                staff_role,
                wins,
                losses,
                ties
            )
            SELECT
                t.staff_id,
                t.year,
                t.team,
                t.role,
                t.wins,
                t.losses,
                t.ties
            FROM {table_name} t
            ;
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