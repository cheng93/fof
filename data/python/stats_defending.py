from base_stats import BaseStats
from collections import namedtuple
import csv
import os


class StatsDefending(BaseStats):
    def __init__(self):
        self.stats = [
            "Tackles",
            "Assists",
            "Sacks_x",
            "Interceptions",
            "Interception_Return_Yards",
            "Interception_Return_Touchdowns",
            "Passes_Defensed",
            "Passes_Blocked",
            "Hurries",
            "Caught_Against",
            "Pass_Plays",
            "Run_Plays"
        ]

    def execute(self, cursor, year):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            df["Stage_Name"] = df.apply(lambda x: self.get_stage(x).name, axis=1)
            df["Stage_Type"] = df.apply(lambda x: self.get_stage(x).type, axis=1)
            df["Year"] = year
            df["Sacks_x"] = df["Sacks_(x10)"].apply(lambda x: x / 10)
            query = " != 0 or ".join(self.stats)
            df = df.query(query)
            return df

        file_name = f"player_season_{int(year) - 1}.csv"

        table_name = "temp_stats_defending"
        table_definition = """
            temp_stats_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            team SMALLINT,
            year SMALLINT,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50),
            tackles REAL,
            assists REAL,
            sacks_x REAL,
            interceptions SMALLINT,
            interception_return_yards INTEGER,
            interception_return_touchdowns SMALLINT,
            passes_defensed SMALLINT,
            passes_blocked SMALLINT,
            hurries SMALLINT,
            caught_against SMALLINT,
            pass_plays SMALLINT,
            run_plays SMALLINT
        """

        columns = [
            "Player_ID",
            "Team",
            "Year",
            "Stage_Name",
            "Stage_Type"
        ]

        columns = columns + self.stats

        migrate_sql = f"""
            INSERT INTO stats.defending
            (
                player_id,
                game_id,
                team_id,
                tackles,
                assists,
                sacks,
                interception,
                interception_yards,
                interception_touchdowns,
                passes_defended,
                passes_blocked,
                hurries,
                caught_against,
                pass_plays,
                run_plays
            )
            SELECT
                t.player_id,
                g.game_id,
                t.team,
                t.tackles,
                t.assists,
                t.sacks_x,
                t.interceptions,
                t.interception_return_yards,
                t.interception_return_touchdowns,
                t.passes_defensed,
                t.passes_blocked,
                t.hurries,
                t.caught_against,
                t.pass_plays,
                t.run_plays
            FROM {table_name} t
                INNER JOIN stage s
                    ON s.stage_name = t.stage_name
                        AND s.stage_type = t.stage_type
                INNER JOIN game g
                    ON g.stage_id = s.stage_id
                        AND g.year = t.year
                        AND (
                            g.home_team_id = t.team
                            OR g.visitor_team_id = t.team
                        )
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
