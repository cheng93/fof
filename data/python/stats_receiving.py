from base_stats import BaseStats
from collections import namedtuple
import csv
import os


class StatsReceiving(BaseStats):
    def __init__(self):
        self.stats = [
            "Catches",
            "Receiving_Yards",
            "Long_Reception",
            "Receiving_Touchdowns",
            "Targets",
            "Yards_after_Catch",
            "Drops"
        ]

    def execute(self, cursor, year):
        def manipulate_df(df, **kwargs):
            year = kwargs["year"]
            df["Stage_Name"] = df.apply(lambda x: self.get_stage(x).name, axis=1)
            df["Stage_Type"] = df.apply(lambda x: self.get_stage(x).type, axis=1)
            df["Year"] = year
            query = " != 0 or ".join(self.stats)
            df = df.query(query)
            return df

        file_name = f"player_season_{int(year) - 1}.csv"

        table_name = "temp_stats_receiving"
        table_definition = """
            temp_stats_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            team SMALLINT,
            year SMALLINT,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50),
            catches SMALLINT,
            receiving_yards INTEGER,
            long_reception SMALLINT,
            receiving_touchdowns SMALLINT,
            targets SMALLINT,
            yards_after_catch INTEGER,
            drops SMALLINT
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
            INSERT INTO stats.receiving
            (
                player_id,
                game_id,
                team_id,
                catches,
                yards,
                longest,
                touchdowns,
                targets,
                yards_after_catch,
                drops
            )
            SELECT
                t.player_id,
                g.game_id,
                t.team,
                t.catches,
                t.receiving_yards,
                t.long_reception,
                t.receiving_touchdowns,
                t.targets,
                t.yards_after_catch,
                t.drops
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
