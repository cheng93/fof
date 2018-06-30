"""team_season_summary

Revision ID: cd25094e20e1
Revises: a49e44652c48
Create Date: 2018-06-30 13:58:19.655708

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd25094e20e1'
down_revision = 'a49e44652c48'
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
    op.execute("""
        CREATE VIEW team_season_summary
        AS
        SELECT
            t.team_id,
            g."year",
            CAST(COUNT(st.win) AS smallint) wins,
            CAST(COUNT(st.lose) AS smallint) loses,
            CAST(COUNT(st.tie) AS smallint) ties,
            COUNT(st.win) / CAST(COUNT(st.non_tie) AS decimal) win_lose_percent
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
                END home_result
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
        GROUP BY t.team_id, g."year"
        ;
    """)
    pass


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.execute("""
        DROP VIEW team_season_summary
    """)
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
