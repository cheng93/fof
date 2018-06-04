from base_fof import BaseFof
import csv
import os


class Player(BaseFof):
    def execute(self, cursor, year):
        def manipulate_player_df(df, **kwargs):
            year = kwargs["year"]
            df["Birth_Date"] = df.apply(get_birth_date, axis=1)
            df["Stage_Name"] = "Draft"
            df["Stage_Type"] = "Pre Season"
            df["Year"] = int(year)
            df = df.query("Season_1_Year == 0")
            return df

        file_name="player_information.csv"

        table_name = "temp_player"
        table_definition = """
            temp_player_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            last_name VARCHAR(126),
            first_name VARCHAR(126),
            position VARCHAR(4),
            height SMALLINT,
            weight SMALLINT,
            birth_date DATE
        """

        columns=[
            "Player_ID",
            "Last_Name",
            "First_Name",
            "Position",
            "Height",
            "Weight",
            "Birth_Date"
        ]

        migrate_sql = f"""
            INSERT INTO player
            (
                player_id,
                last_name,
                first_name,
                position,
                height,
                weight,
                birth_date
            )
            SELECT
                t.player_id,
                t.last_name,
                t.first_name,
                t.position,
                t.height,
                t.weight,
                t.birth_date
            FROM {table_name} t
        """

        super().execute(
            cursor=cursor,
            year=year,
            file_name=file_name,
            manipulate_df=manipulate_player_df,
            table_name=table_name,
            table_definition=table_definition,
            columns=columns,
            migrate_sql=migrate_sql)

        def manipulate_player_history_df(df, **kwargs):
            df = manipulate_player_df(df, **kwargs)
            df = df.query("Draft_Year != 0")
            return df

        table_name = "temp_player_history"
        table_definition = """
            temp_player_history_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            year SMALLINT,
            drafted_by SMALLINT,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50)
        """

        columns=[
            "Player_ID",
            "Year",
            "Drafted_By",
            "Stage_Name",
            "Stage_Type"
        ]

        migrate_sql = f"""
            INSERT INTO player_history
            (
                player_id,
                year,
                stage_id,
                new_team_id
            )
            SELECT 
                t.player_id,
                t.year,
                s.stage_id,
                t.drafted_by
            FROM {table_name} t
                INNER JOIN stage s
                    ON s.stage_name = t.stage_name
                        AND s.stage_type = t.stage_type
        """

        super().execute(
            cursor=cursor,
            year=year,
            file_name=file_name,
            manipulate_df=manipulate_player_history_df,
            table_name=table_name,
            table_definition=table_definition,
            columns=columns,
            migrate_sql=migrate_sql)

def get_birth_date(row):
    return f"{row['Year_Born']}-{row['Month_Born']}-{row['Day_Born']}"    
