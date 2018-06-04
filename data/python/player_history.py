from base_fof import BaseFof
from collections import namedtuple
import csv
import os


class PlayerHistory(BaseFof):
    def execute(self, cursor, year):
        def manipulate_player_history_df(df, **kwargs):
            year = kwargs["year"]
            df["Year"] = int(year) +1
            df["Stage_Name"] = "Pre Free Agency"
            df["Stage_Type"] = "Pre Season"
            df = df.query("Contract_Length == 1")
            return df

        file_name = "player_record.csv"

        table_name = "temp_player_history"
        table_definition = """
            temp_player_history_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            year SMALLINT,
            team SMALLINT,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50)
        """

        columns=[
            "Player_ID",
            "Year",
            "Team",
            "Stage_Name",
            "Stage_Type"
        ]

        migrate_sql = f"""
            INSERT INTO player_history
            (
                player_id,
                year,
                stage_id,
                old_team_id
            )
            SELECT
                t.player_id,
                t.year,
                s.stage_id,
                t.team
            FROM temp_player_history t
                INNER JOIN stage s
                    ON s.stage_name = t.stage_name
                        AND s.stage_type = t.stage_type
            ;
        """

        if year != "2015":
            super().execute(
                cursor=cursor,
                year=int(year) -1,
                file_name=file_name,
                manipulate_df=manipulate_player_history_df,
                table_name=table_name,
                table_definition=table_definition,
                columns=columns,
                migrate_sql=migrate_sql)

        def manipulate_transaction_df(df, **kwargs):
            year = kwargs["year"]
            df["Stage_Name"] = df.apply(lambda x: get_stage(x).name, axis=1)
            df["Stage_Type"] = df.apply(lambda x: get_stage(x).type, axis=1)
            df["Old"] = df.apply(lambda x: get_team(x).old, axis=1)
            df["New"] = df.apply(lambda x: get_team(x).new, axis=1)
            df["Year"] = year
            df["Player_ID"] = df["Player_ID/Staff_ID/Round"]
            transactions = [
                "designated as a franchise player",
                "re-signed as an unrestricted free agent",
                "released",
                "retired",
                "signed as a free agent",
                "signed as an unrestricted free agent"
            ]
            df = df[df["Transaction"].isin(transactions)]

            return df

        file_name = f"transactions_{int(year) -1}.csv"

        table_name = "temp_player_history"
        table_definition = """
            temp_player_history_id SERIAL PRIMARY KEY,
            player_id INTEGER,
            year SMALLINT,
            old SMALLINT NULL,
            new SMALLINT NULL,
            stage_name VARCHAR(50),
            stage_type VARCHAR(50)
        """

        columns = [
            "Player_ID",
            "Year",
            "Old",
            "New",
            "Stage_Name",
            "Stage_Type"
        ]

        migrate_sql = f"""
            INSERT INTO player_history
            (
                player_id,
                year,
                stage_id,
                old_team_id,
                new_team_id
            )
            SELECT 
                t.player_id,
                t.year,
                s.stage_id,
                t.old,
                t.new
            FROM temp_player_history t
                INNER JOIN stage s
                    ON s.stage_name = t.stage_name
                        AND s.stage_type = t.stage_type
            ;
        """

        usecols = [0,1,2,3,4,5,6,7,8]
        super().execute(
            cursor=cursor,
            year=year,
            file_name=file_name,
            manipulate_df=manipulate_transaction_df,
            table_name=table_name,
            table_definition=table_definition,
            columns=columns,
            migrate_sql=migrate_sql,
            usecols=usecols)

def get_stage(row):
    week = row["Stage"]
    stage = namedtuple("stage", ["name", "type"])
    exhibition = "Ex. Season "
    regular = "Reg. Season "
    pre_staff_draft = "Pre-Staff Draft"
    free_agency = "FA Stage "
    late_free_agency = "Late FA Stage "
    pre_training_camp = "Pre-Training Camp"

    pre_season = "Pre Season"
    if week == pre_staff_draft:
        stage.type = pre_season
        stage.name = "Pre Free Agency"
    elif week.startswith(free_agency):
        stage.type = pre_season
        stage.name = "Free Agency"
    elif week.startswith(late_free_agency):
        stage.type = pre_season
        stage.name = "Late Free Agency"
    elif week == pre_training_camp:
        stage.type = pre_season
        stage.name = "Training Camp"
    elif week.startswith(exhibition):
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

def get_team(row):
    transaction = row["Transaction"]
    team_id = row["Team"]
    team = namedtuple("team", ["old", "new"])

    old_transaction = [
        "released",
        "retired"
    ]
    new_transaction = [
        "designated as a franchise player",
        "re-signed as an unrestricted free agent",
        "signed as a free agent",
        "signed as an unrestricted free agent"
    ]
    if transaction in new_transaction:
        team.old = "NULL"
        team.new = team_id
    elif transaction in old_transaction:
        team.old = team_id
        team.new = "NULL"
    return team