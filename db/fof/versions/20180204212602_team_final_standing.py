"""team_final_standing

Revision ID: 827930aa3086
Revises: 4b606814baf3
Create Date: 2018-02-04 21:26:02.651267

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827930aa3086'
down_revision = '8e4ccee543a5'
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
        CREATE VIEW team_final_standing
        AS
        SELECT
            t.team_id,
            t.year,
            CASE MAX(t.final_standing_rank)
                WHEN 0 THEN 'Regular'
                WHEN 1 THEN 'Wildcard'
                WHEN 2 THEN 'Divisional'
                WHEN 3 THEN 'Conference'
                WHEN 4 THEN 'Runner Up'
                WHEN 5 THEN 'Winner'
            END standing_name
        FROM (
            SELECT
                t.team_id,
                g.year,
                s.final_standing_rank
            FROM team t
                INNER JOIN game g
                    ON g.home_team_id = t.team_id
                        OR g.visitor_team_id = t.team_id
                CROSS JOIN LATERAL (
                    SELECT
                        CASE
                            WHEN t.team_id = g.home_team_id
                            THEN true
                            ELSE false
                        END is_home
                ) i
                CROSS JOIN LATERAL (
                    SELECT
                        CASE g.stage_id
                            WHEN 22 THEN 0
                            WHEN 23 THEN 1
                            WHEN 24 THEN 2
                            WHEN 25 THEN 3
                            WHEN 26 THEN
                                CASE 
                                    WHEN (
                                            i.is_home = true
                                            AND g.home_score > g.visitor_score
                                        )
                                        OR (
                                            i.is_home = false
                                            AND g.home_score < g.visitor_score
                                        )
                                    THEN 5
                                    ELSE 4
                                END
                        END final_standing_rank
                ) s
        ) t
        GROUP BY t.team_id, t.year
        ;
    """)
    pass


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.execute("""
        DROP VIEW team_final_standing
        ;
    """)
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
