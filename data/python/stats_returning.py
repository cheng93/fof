from base_stats import BaseStats
from collections import namedtuple
import csv
import os


class StatsReturning(BaseStats):
    def __init__(self):
        self.stats = [
            "Punt_Returns",
            "Punt_Return_Yards",
            "Punt_Returns_Touchdowns",
            "Kick_Returns",
            "Kick_Return_Yards",
            "Kick_Return_Touchdowns"
        ]

    def execute(self, cursor, year):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            query = " != 0 or ".join(self.stats)
            df = df.query(query).copy(deep=True)
            df["Stage_Name"] = self.get_stage_name_vectorized(df['Week'])
            df["Stage_Type"] = self.get_stage_type_vectorized(df['Week'])
            df["Year"] = year
            return df

        file_name = f"player_season_{int(year) - 1}.csv"

        table_name = "temp_stats_returning"
        table_definition = """
            temp_stats_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            team SMALLINT,
            year SMALLINT,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50),
            punt_returns SMALLINT,
            punt_return_yards INTEGER,
            punt_returns_touchdowns SMALLINT,
            kick_returns SMALLINT,
            kick_return_yards INTEGER,
            kick_return_touchdowns SMALLINT
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
            INSERT INTO stats.returning
            (
                player_id,
                game_id,
                team_id,
                punt_returns,
                punt_return_yards,
                punt_return_touchdowns,
                kick_returns,
                kick_return_yards,
                kick_return_touchdowns
            )
            SELECT
                t.player_id,
                g.game_id,
                t.team,
                t.punt_returns,
                t.punt_return_yards,
                t.punt_returns_touchdowns,
                t.kick_returns,
                t.kick_return_yards,
                t.kick_return_touchdowns
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
