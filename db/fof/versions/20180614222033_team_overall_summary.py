"""team_overall_summary

Revision ID: a49e44652c48
Revises: b451463927b0
Create Date: 2018-06-14 22:20:33.154930

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a49e44652c48'
down_revision = 'b451463927b0'
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
        CREATE VIEW team_overall_summary
        AS
        SELECT
            s.team_id,
            t.team_name,
            t.city,
            CAST(s.wins as smallint) wins,
            CAST(s.loses as smallint) loses,
            CAST(s.ties as smallint) ties,
            s.win_lose_percent,
            CAST(s.conference_wins AS smallint) conference_wins,
            CAST(s.superbowl_wins AS smallint) superbowl_wins,
            CAST(p.playoff_appearances AS smallint) playoff_appearances
        FROM team t
            INNER JOIN (
                SELECT
                    t.team_id,
                    COUNT(st.win) wins,
                    COUNT(st.lose) loses,
                    COUNT(st.tie) ties,
                    COUNT(st.win) / CAST(COUNT(st.non_tie) AS decimal) win_lose_percent,
                    COUNT(pl.conference_win) conference_wins,
                    COUNT(pl.superbowl_win) superbowl_wins
                FROM team t 
                    INNER JOIN game g
                        ON g.home_team_id = t.team_id
                            OR g.visitor_team_id = t.team_id
                    INNER JOIN stage s
                        ON s.stage_id = g.stage_id
                    CROSS JOIN LATERAL (
                        SELECT 
                            CASE 
                                WHEN g.home_team_id = t.team_id THEN TRUE 
                                ELSE FALSE 
                            END is_home,
                            CASE
                                WHEN g.home_score > g.visitor_score THEN 'W'
                                WHEN g.home_score = g.visitor_score THEN 'T'
                                WHEN g.home_score < g.visitor_score THEN 'L'
                            END home_result,
                            CASE
                                WHEN s.stage_id = 25 THEN TRUE
                                ELSE FALSE
                            END is_conference,
                            CASE
                                WHEN s.stage_id = 26 THEN TRUE
                                ELSE FALSE
                            END is_superbowl
                    ) ha
                    CROSS JOIN LATERAL (
                        SELECT
                            CASE 
                                WHEN (ha.is_home AND ha.home_result = 'W') 
                                    OR (ha.is_home = FALSE AND ha.home_result = 'L') 
                                THEN g.game_id
                            END win,			
                            CASE 
                                WHEN (ha.is_home = FALSE AND ha.home_result = 'W') 
                                    OR (ha.is_home AND ha.home_result = 'L') 
                                THEN g.game_id
                            END lose,
                            CASE
                                WHEN ha.home_result = 'T'
                                THEN g.game_id
                            END tie,
                            CASE
                                WHEN ha.home_result != 'T'
                                THEN g.game_id
                            END non_tie
                    ) st
                    CROSS JOIN LATERAL (
                        SELECT
                            CASE WHEN ha.is_conference AND st.win IS NOT NULL THEN g.game_id END conference_win,
                            CASE WHEN ha.is_superbowl AND st.win IS NOT NULL THEN g.game_id END superbowl_win
                    ) pl
                GROUP BY t.team_id
            ) s
                ON s.team_id = t.team_id
            INNER JOIN (
                SELECT
                    t.team_id,
                    COUNT(DISTINCT pg."year") AS playoff_appearances
                FROM team t 
                    LEFT JOIN (
                        SELECT 
                            g.game_id,
                            g."year",
                            g.home_team_id,
                            g.visitor_team_id
                        FROM game g
                        WHERE
                            EXISTS (
                                SELECT NULL
                                FROM stage s
                                WHERE s.stage_id = g.stage_id
                                    AND s.stage_type = 'Playoffs'
                            )
                    ) pg
                        ON pg.home_team_id = t.team_id
                            OR pg.visitor_team_id = t.team_id
                GROUP BY t.team_id
            ) p	
                ON p.team_id = t.team_id
        ;
    """)
    pass


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.execute("""
        DROP VIEW team_overall_summary
        ;
    """)
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
