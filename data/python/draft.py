from base_fof import BaseFof
import csv
import operator
import os


class Draft(BaseFof):
    def execute(self, cursor, year):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            df["Year"] = int(year)
            df = df.query(f"Draft_Year == {int(year)-1}")
            df = df.sort_values(["Draft_Year", "Draft_Round", "Drafted_Position"], ascending=[1, 1, 1])
            return df

        file_name="player_information.csv"
       
        table_name = "temp_draft"
        table_definition = """
            temp_draft_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            year SMALLINT,
            draft_round SMALLINT,
            drafted_position SMALLINT,
            drafted_by SMALLINT
        """
        columns=[
            "Player_ID",
            "Year",
            "Draft_Round",
            "Drafted_Position",
            "Drafted_By"
        ]

        migrate_sql = f"""
            INSERT INTO draft
            (
                year,
                round,
                pick,
                player_id,
                team_id
            )
            SELECT
                t.year,
                t.draft_round,
                t.drafted_position,
                t.player_id,
                t.drafted_by
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
