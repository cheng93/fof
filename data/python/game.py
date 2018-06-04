from base_fof import BaseFof
import collections
import csv
import os


class Game(BaseFof):
    def execute(self, cursor, year):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            df["Stage_Name"] = df.apply(lambda x: get_stage(x).name, axis=1)
            df["Stage_Type"] = df.apply(lambda x: get_stage(x).type, axis=1)
            df["Year"] = df.apply(lambda x: int(x["Year"]) +1, axis=1)
            df = df.query(f"Year == {year}")
            return df

        file_name="game_information.csv"

        table_name = "temp_game"
        table_definition = """
            temp_game_id SERIAL PRIMARY KEY,
            year SMALLINT,
            home_team SMALLINT,
            home_score SMALLINT,
            visitor_team SMALLINT,
            visitor_score SMALLINT,
            attendance INTEGER,
            weather VARCHAR(50),
            wind REAL,
            temperature REAL,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50)
        """

        columns=[
            "Year",
            "Home_Team",
            "Home_Score",
            "Visitor_Team",
            "Visitor_Score",
            "Attendance",
            "Weather",
            "Wind",
            "Temperature",
            "Stage_Name",
            "Stage_Type"
        ]

        migrate_sql = f"""
            INSERT INTO game
            (
                year,
                stage_id,
                home_team_id,
                home_score,
                visitor_team_id,
                visitor_score,
                attendance,
                weather,
                wind,
                temperature
            )
            SELECT
                t.year,
                s.stage_id,
                t.home_team,
                t.home_score,
                t.visitor_team,
                t.visitor_score,
                t.attendance,
                t.weather,
                t.wind,
                t.temperature
            FROM {table_name} t
                INNER JOIN stage s
                    ON s.stage_name = t.stage_name
                        AND s.stage_type = t.stage_type 
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

def get_stage(row):
    week = row["Week"]
    stage = collections.namedtuple("stage", ["name", "type"])
    exhibition = "Ex. Season "
    regular = "Reg. Season "
    if week.startswith(exhibition):
        stage.type = "Exhibition"
        stage.name = week[len(exhibition):]
    elif week.startswith(regular):
        stage.type = "Regular"
        stage.name = week[len(regular):]
    else:
        stage.type = "Playoffs"
        if week == "Wild Card Round":
            stage.name = "Wildcard"
        elif week == "Divisional Round":
            stage.name = "Divisional"
        elif week == "Conference Round":
            stage.name = "Conference"
        else:
            stage.name = "Superbowl"    
    return stage
