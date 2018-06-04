"""player_latest_team

Revision ID: 71797fe46b5c
Revises: 827930aa3086
Create Date: 2018-02-11 18:49:34.688616

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71797fe46b5c'
down_revision = '827930aa3086'
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
        CREATE VIEW player_latest_team
        AS
        SELECT
            ph.player_id,
            ph.new_team_id AS team_id
        FROM (
            SELECT
                ph.player_id,
                ph.new_team_id,
                DENSE_RANK() OVER (PARTITION BY ph.player_id ORDER BY ph.year DESC, st.rank DESC, s.rank DESC) AS rank
            FROM player_history ph
                INNER JOIN stage s
                    ON s.stage_id = ph.stage_id
                INNER JOIN stage_type st
                    ON st.stage_type = s.stage_type
        ) ph
        WHERE
            ph.rank = 1
        ;
    """)
    pass


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.execute("""
        DROP VIEW player_latest_team
        ;
    """)
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
