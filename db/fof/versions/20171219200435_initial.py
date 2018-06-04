"""initial

Revision ID: 8e4ccee543a5
Revises: 
Create Date: 2017-12-19 20:04:35.331450

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e4ccee543a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('seed', None):
        data_upgrades()


def downgrade():
    data_downgrades()
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    op.execute("""
        CREATE TABLE team
        (
            team_id SMALLINT NOT NULL
                CONSTRAINT team_pkey
                    PRIMARY KEY,
            city VARCHAR(50) NOT NULL,
            team_name VARCHAR(50) NOT NULL
        )
        ;

        CREATE TABLE year
        (
            year SMALLINT NOT NULL
                CONSTRAINT year_pkey
                    PRIMARY KEY
        )
        ;

        CREATE TABLE stage_type
        (
            stage_type VARCHAR(50) NOT NULL
                CONSTRAINT stage_type_pkey
                    PRIMARY KEY,
            rank SMALLINT NOT NULL
                CONSTRAINT stage_type_rank_unq UNIQUE
        )
        ;

        CREATE SEQUENCE stage_stage_id_seq
        ;

        CREATE TABLE stage
        (
            stage_id SMALLINT DEFAULT NEXTVAL('stage_stage_id_seq'::regClass) NOT NULL
                CONSTRAINT stage_pkey
                    PRIMARY KEY,
            stage_name VARCHAR(50) NOT NULL,
            stage_type VARCHAR(50) NOT NULL
                CONSTRAINT stage_stage_type_fkey
                    REFERENCES stage_type
                        ON UPDATE CASCADE,
            rank SMALLINT NOT NULL,
            CONSTRAINT stage_stage_type_rank_uq
                UNIQUE(stage_type, rank)
        )
        ;

        CREATE TABLE position
        (
            position VARCHAR(4) NOT NULL
                CONSTRAINT position_pkey
                    PRIMARY KEY
        )
        ;

        CREATE SEQUENCE game_game_id_seq
        ;

        CREATE TABLE game
        (
            game_id INTEGER DEFAULT NEXTVAL('game_game_id_seq'::regClass) NOT NULL
                CONSTRAINT game_pkey
                    PRIMARY KEY,
            year SMALLINT NOT NULL
                CONSTRAINT game_year_fkey
                    REFERENCES year,
            stage_id SMALLINT NOT NULL
                CONSTRAINT game_stage_id_fkey
                    REFERENCES stage,
            home_team_id SMALLINT NOT NULL
                CONSTRAINT game_home_team_id_fkey
                    REFERENCES team
                        ON UPDATE CASCADE,
            home_score SMALLINT NOT NULL,
            visitor_team_id SMALLINT NOT NULL
                CONSTRAINT game_visitor_team_id_fkey
                    REFERENCES team
                        ON UPDATE CASCADE,
            visitor_score SMALLINT NOT NULL,
            attendance INTEGER,
            weather VARCHAR(50),
            wind REAL,
            temperature REAL,
            CONSTRAINT game_home_team_id_visitor_team_id_chk
                CHECK (home_team_id != visitor_team_id)
        )
        ;

        CREATE TABLE player
        (
            player_id INTEGER NOT NULL
                CONSTRAINT player_player_id_pkey
                    PRIMARY KEY,
            last_name VARCHAR(126) NOT NULL,
            first_name VARCHAR(126) NOT NULL,
            position VARCHAR(4) NOT NULL
                CONSTRAINT player_position_fkey
                    REFERENCES position
                        ON UPDATE CASCADE,
            height SMALLINT NOT NULL,
            weight SMALLINT NOT NULL,
            birth_date DATE NOT NULL
        )
        ;

        CREATE TABLE draft
        (
            year SMALLINT NOT NULL
                CONSTRAINT draft_year_fkey
                    REFERENCES year,
            round SMALLINT NOT NULL,
            pick SMALLINT NOT NULL,
            player_id INTEGER NOT NULL
                CONSTRAINT draft_player_id_fkey
                    REFERENCES player,
            team_id SMALLINT NOT NULL
                CONSTRAINT draft_team_id_fkey
                    REFERENCES team,
            CONSTRAINT draft_pkey
                PRIMARY KEY (year, round, pick)
        )
        ;

        CREATE TABLE staff_group
        (
            staff_group VARCHAR(50) NOT NULL
                CONSTRAINT staff_group_pkey
                    PRIMARY KEY
        )
        ;

        CREATE TABLE staff
        (
            staff_id INTEGER NOT NULL
                CONSTRAINT staff_pkey
                    PRIMARY KEY,
            last_name VARCHAR(126) NOT NULL,
            first_name VARCHAR(126) NOT NULL,
            birth_year SMALLINT NOT NULL,
            staff_group VARCHAR(50) NOT NULL
                CONSTRAINT staff_staff_group_fkey
                    REFERENCES staff_group
        )
        ;

        CREATE TABLE staff_role
        (
            staff_role VARCHAR(50) NOT NULL
                CONSTRAINT staff_role_pkey
                    PRIMARY KEY
        )
        ;

        CREATE TABLE staff_history
        (
            staff_id INTEGER NOT NULL
                CONSTRAINT staff_history_staff_id_fkey
                    REFERENCES staff,
            year SMALLINT NOT NULL
                CONSTRAINT staff_history_year_fkey
                    REFERENCES year,
            team_id SMALLINT NOT NULL
                CONSTRAINT staff_history_team_id_fkey
                    REFERENCES team,
            staff_role VARCHAR(50) NOT NULL
                CONSTRAINT staff_history_staff_role_fkey
                    REFERENCES staff_role,
            wins SMALLINT NOT NULL,
            losses SMALLINT NOT NULL,
            ties SMALLINT NOT NULL,
            CONSTRAINT staff_history_pkey
                PRIMARY KEY (staff_id, year)
        )
        ;

        CREATE SEQUENCE player_history_player_history_id_seq
        ;

        CREATE TABLE player_history
        (
            player_history_id INTEGER DEFAULT NEXTVAL('player_history_player_history_id_seq'::regClass) NOT NULL
                CONSTRAINT player_history_pkey
                    PRIMARY KEY,
            player_id INTEGER NOT NULL
                CONSTRAINT player_history_player_id_fkey
                    REFERENCES player,
            year SMALLINT NOT NULL
                CONSTRAINT player_history_year_fkey
                    REFERENCES year,
            stage_id SMALLINT NOT NULL
                CONSTRAINT player_history_stage_id_fkey
                    REFERENCES stage,
            old_team_id SMALLINT NULL
                CONSTRAINT player_history_old_team_id_fkey
                    REFERENCES team,
            new_team_id SMALLINT NULL
                CONSTRAINT player_history_new_team_id_fkey
                    REFERENCES team
        )
        ;

        CREATE SCHEMA stats
        ;

        CREATE TABLE stats.passing
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_passing_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_passing_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_passing_team_id_fkey
                    REFERENCES public.team,
            attempts SMALLINT NOT NULL,
            completions SMALLINT NOT NULL,
            yards INTEGER NOT NULL,
            longest SMALLINT NOT NULL,
            touchdowns SMALLINT NOT NULL,
            interceptions SMALLINT NOT NULL,
            CONSTRAINT stats_passing_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.rushing
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_rushing_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_rushing_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_rushing_team_id_fkey
                    REFERENCES public.team,
            attempts SMALLINT NOT NULL,
            yards INTEGER NOT NULL,
            longest SMALLINT NOT NULL,
            touchdowns SMALLINT NOT NULL,
            CONSTRAINT stats_rushing_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.receiving
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_receiving_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_receiving_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_receiving_team_id_fkey
                    REFERENCES public.team,
            targets SMALLINT NOT NULL,
            catches SMALLINT NOT NULL,
            drops SMALLINT NOT NULL,
            yards INTEGER NOT NULL,
            longest SMALLINT NOT NULL,
            touchdowns SMALLINT NOT NULL,
            yards_after_catch INTEGER NOT NULL,
            CONSTRAINT stats_receiving_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.returning
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_returning_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_returning_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_returning_team_id_fkey
                    REFERENCES public.team,
            punt_returns SMALLINT NOT NULL,
            punt_return_yards INTEGER NOT NULL,
            punt_return_touchdowns SMALLINT NOT NULL,
            kick_returns SMALLINT NOT NULL,
            kick_return_yards INTEGER NOT NULL,
            kick_return_touchdowns SMALLINT NOT NULL,
            CONSTRAINT stats_punt_return_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.fumbles
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_fumbles_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_fumbles_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_fumbles_team_id_fkey
                    REFERENCES public.team,
            lost SMALLINT NOT NULL,
            recovered SMALLINT NOT NULL,
            forced SMALLINT NOT NULL,
            touchdowns SMALLINT NOT NULL,
            CONSTRAINT stats_fumbles_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.blocking
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_blocking_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_blocking_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_blocking_team_id_fkey
                    REFERENCES public.team,
            key SMALLINT NOT NULL,
            opportunities SMALLINT NOT NULL,
            sacks_allowed SMALLINT NOT NULL,
            CONSTRAINT stats_blocking_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.defending
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_defending_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_defending_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_defending_team_id_fkey
                    REFERENCES public.team,
            tackles SMALLINT NOT NULL,
            assists SMALLINT NOT NULL,
            sacks float NOT NULL,
            interception SMALLINT NOT NULL,
            interception_yards INTEGER NOT NULL,
            interception_touchdowns SMALLINT NOT NULL,
            passes_defended SMALLINT NOT NULL,
            passes_blocked SMALLINT NOT NULL,
            hurries SMALLINT NOT NULL,
            caught_against SMALLINT NOT NULL,
            pass_plays SMALLINT NOT NULL,
            run_plays SMALLINT NOT NULL,
            CONSTRAINT stats_defending_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.kicking
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_kicking_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_kicking_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_kicking_team_id_fkey
                    REFERENCES public.team,
            field_goals SMALLINT NOT NULL,
            field_goals_attempts SMALLINT NOT NULL,
            longest_field_goal SMALLINT NOT NULL,
            pats SMALLINT NOT NULL,
            pats_attempts SMALLINT NOT NULL,
            CONSTRAINT stats_kicking_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;

        CREATE TABLE stats.punting
        (
            player_id INTEGER NOT NULL
                CONSTRAINT stats_punting_player_id_fkey
                    REFERENCES public.player,
            game_id INTEGER NOT NULL
                CONSTRAINT stats_punting_game_id_fkey
                    REFERENCES public.game,
            team_id SMALLINT NOT NULL
                CONSTRAINT stats_punting_team_id_fkey
                    REFERENCES public.team,
            attempts SMALLINT NOT NULL,
            yards INTEGER NOT NULL,
            longest SMALLINT NOT NULL,
            inside_twenty SMALLINT NOT NULL,
            CONSTRAINT stats_punting_pkey
                PRIMARY KEY (player_id, game_id)
        )
        ;
    """)
    pass


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.execute("""
        DROP TABLE stats.punting
        ;

        DROP TABLE stats.kicking
        ;

        DROP TABLE stats.defending
        ;

        DROP TABLE stats.blocking
        ;

        DROP TABLE stats.fumbles
        ;

        DROP TABLE stats.returning
        ;

        DROP TABLE stats.receiving
        ;

        DROP TABLE stats.rushing
        ;

        DROP TABLE stats.passing
        ;

        DROP SCHEMA stats
        ;

        DROP TABLE player_history
        ;

        DROP SEQUENCE player_history_player_history_id_seq
        ;

        DROP TABLE staff_history
        ;

        DROP TABLE staff_role
        ;

        DROP TABLE staff
        ;

        DROP TABLE staff_group
        ;

        DROP TABLE draft
        ;

        DROP TABLE player
        ;

        DROP TABLE game
        ;

        DROP SEQUENCE game_game_id_seq
        ;

        DROP TABLE position
        ;

        DROP TABLE stage
        ;

        DROP SEQUENCE stage_stage_id_seq
        ;

        DROP TABLE stage_type
        ;

        DROP TABLE year
        ;

        DROP TABLE team
        ;
    """)
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    op.execute("""
        INSERT INTO team (team_id, city, team_name)
        VALUES (0, 'Arizona', 'Cardinals')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (1, 'Atlanta', 'Falcons')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (2, 'Baltimore', 'Ravens')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (3, 'Buffalo', 'Bills')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (4, 'Carolina', 'Panthers')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (5, 'Chicago', 'Bears')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (6, 'Cincinnati', 'Bengals')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (7, 'Dallas', 'Cowboys')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (8, 'Denver', 'Broncos')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (9, 'Detroit', 'Lions')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (10, 'Green Bay', 'Packers')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (11, 'Indianapolis', 'Colts')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (12, 'Jacksonville', 'Jaguars')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (13, 'Kansas City', 'Chiefs')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (14, 'Miami', 'Dolphins')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (15, 'Minnesota', 'Vikings')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (16, 'New England', 'Patriots')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (17, 'New Orleans', 'Saints')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (18, 'New York', 'Giants')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (19, 'New Jersey', 'Jets')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (20, 'Oakland', 'Raiders')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (21, 'Philadelphia', 'Eagles')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (22, 'Pittsburgh', 'Steelers')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (23, 'San Diego', 'Chargers')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (24, 'Seattle', 'Seahawks')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (25, 'San Francisco', '49ers')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (26, 'St. Louis', 'Rams')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (27, 'Tampa Bay', 'Buccaneers')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (28, 'Tennessee', 'Titans')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (29, 'Washington', 'Redskins')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (30, 'Cleveland', 'Browns')
        ;

        INSERT INTO team (team_id, city, team_name)
        VALUES (31, 'Houston', 'Texans')
        ;

        INSERT INTO stage_type (stage_type, rank)
        VALUES ('Pre Season', 0)
        ;

        INSERT INTO stage_type (stage_type, rank)
        VALUES ('Exhibition', 10)
        ;

        INSERT INTO stage_type (stage_type, rank)
        VALUES ('Regular', 20)
        ;

        INSERT INTO stage_type (stage_type, rank)
        VALUES ('Playoffs', 30)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 1', 'Exhibition', 0)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 2', 'Exhibition', 10)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 3', 'Exhibition', 20)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 4', 'Exhibition', 30)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 5', 'Exhibition', 40)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 1', 'Regular', 0)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 2', 'Regular', 10)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 3', 'Regular', 20)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 4', 'Regular', 30)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 5', 'Regular', 40)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 6', 'Regular', 50)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 7', 'Regular', 60)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 8', 'Regular', 70)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 9', 'Regular', 80)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 10', 'Regular', 90)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 11', 'Regular', 100)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 12', 'Regular', 110)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 13', 'Regular', 120)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 14', 'Regular', 130)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 15', 'Regular', 140)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 16', 'Regular', 150)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Week 17', 'Regular', 160)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Wildcard', 'Playoffs', 0)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Divisional', 'Playoffs', 10)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Conference', 'Playoffs', 20)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Superbowl', 'Playoffs', 30)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Pre Free Agency', 'Pre Season', 0)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Free Agency', 'Pre Season', 10)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Draft', 'Pre Season', 20)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Late Free Agency', 'Pre Season', 30)
        ;

        INSERT INTO stage (stage_name, stage_type, rank)
        VALUES ('Training Camp', 'Pre Season', 40)
        ;

        INSERT INTO position (position)
        VALUES ('C')
        ;

        INSERT INTO position (position)
        VALUES ('FB')
        ;

        INSERT INTO position (position)
        VALUES ('FL')
        ;

        INSERT INTO position (position)
        VALUES ('FS')
        ;

        INSERT INTO position (position)
        VALUES ('K')
        ;

        INSERT INTO position (position)
        VALUES ('LCB')
        ;

        INSERT INTO position (position)
        VALUES ('LDE')
        ;

        INSERT INTO position (position)
        VALUES ('LDT')
        ;

        INSERT INTO position (position)
        VALUES ('LG')
        ;

        INSERT INTO position (position)
        VALUES ('LS')
        ;

        INSERT INTO position (position)
        VALUES ('LT')
        ;

        INSERT INTO position (position)
        VALUES ('MLB')
        ;

        INSERT INTO position (position)
        VALUES ('NT')
        ;

        INSERT INTO position (position)
        VALUES ('P')
        ;

        INSERT INTO position (position)
        VALUES ('QB')
        ;

        INSERT INTO position (position)
        VALUES ('RB')
        ;

        INSERT INTO position (position)
        VALUES ('RCB')
        ;

        INSERT INTO position (position)
        VALUES ('RDE')
        ;

        INSERT INTO position (position)
        VALUES ('RDT')
        ;

        INSERT INTO position (position)
        VALUES ('RG')
        ;

        INSERT INTO position (position)
        VALUES ('RT')
        ;

        INSERT INTO position (position)
        VALUES ('SE')
        ;

        INSERT INTO position (position)
        VALUES ('SILB')
        ;

        INSERT INTO position (position)
        VALUES ('SLB')
        ;

        INSERT INTO position (position)
        VALUES ('SS')
        ;

        INSERT INTO position (position)
        VALUES ('TE')
        ;

        INSERT INTO position (position)
        VALUES ('WILB')
        ;

        INSERT INTO position (position)
        VALUES ('WLB')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Defensive Linemen')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Linebackers')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Offensive Linemen')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Quarterbacks')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Running Backs')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Secondary')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Strength')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Tight Ends')
        ;

        INSERT INTO staff_group(staff_group)
        VALUES ('Wide Receivers')
        ;

        INSERT INTO staff_role(staff_role)
        VALUES ('Assistant Coach')
        ;

        INSERT INTO staff_role(staff_role)
        VALUES ('Defensive Coordinator')
        ;

        INSERT INTO staff_role(staff_role)
        VALUES ('Head Coach')
        ;

        INSERT INTO staff_role(staff_role)
        VALUES ('Offensive Coordinator')
        ;

        INSERT INTO staff_role(staff_role)
        VALUES ('Strength Coordinator')
        ;

    """)
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
