"""division

Revision ID: b451463927b0
Revises: 71797fe46b5c
Create Date: 2018-03-03 19:59:02.398778

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b451463927b0'
down_revision = '71797fe46b5c'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('seed', None):
        data_upgrades()
        post_data_schema_upgrades()


def downgrade():
    data_downgrades()
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    op.execute("""
        CREATE TABLE conference
        (
            conference_id SMALLINT NOT NULL
                CONSTRAINT conference_pkey
                    PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        )
        ;

        CREATE TABLE division
        (
            division_id SMALLINT NOT NULL
                CONSTRAINT division_pkey
                    PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            conference_id SMALLINT NOT NULL
                CONSTRAINT division_conference_id_fkey
                    REFERENCES conference
                    ON UPDATE CASCADE
        )
        ;

        ALTER TABLE team
        ADD COLUMN division_id SMALLINT
        ;
    """)
    pass


def post_data_schema_upgrades():
    op.execute("""
        ALTER TABLE team
        ALTER COLUMN division_id 
            SET NOT NULL,
        ADD CONSTRAINT team_division_id_fkey
            FOREIGN KEY (division_id)
                REFERENCES division
                ON UPDATE CASCADE
        ;
    """)


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.execute("""
        ALTER TABLE team
        DROP COLUMN division_id
        ;

        DROP TABLE division
        ;

        DROP TABLE conference
        ;
    """)
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    op.execute("""
        INSERT INTO conference (conference_id, name)
        VALUES (0, 'American Conference')
        ;

        INSERT INTO conference (conference_id, name)
        VALUES (1, 'National Conference')
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (0, 'AC North', 0)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (1, 'AC East', 0)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (2, 'AC South', 0)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (3, 'AC West', 0)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (4, 'NC North', 1)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (5, 'NC East', 1)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (6, 'NC South', 1)
        ;

        INSERT INTO division (division_id, name, conference_id)
        VALUES (7, 'NC West', 1)
        ;

        UPDATE team
        SET division_id = 0
        WHERE team_id IN (
            2, 6, 22, 30
        )
        ;

        UPDATE team
        SET division_id = 1
        WHERE team_id IN (
            3, 14, 16, 19
        )
        ;

        UPDATE team
        SET division_id = 2
        WHERE team_id IN (
            11, 12, 28, 31
        )
        ;

        UPDATE team
        SET division_id = 3
        WHERE team_id IN (
            8, 13, 20, 23
        )
        ;

        UPDATE team
        SET division_id = 4
        WHERE team_id IN (
            5, 9, 10, 15
        )
        ;

        UPDATE team
        SET division_id = 5
        WHERE team_id IN (
            7, 18, 21, 29
        )
        ;

        UPDATE team
        SET division_id = 6
        WHERE team_id IN (
            1, 4, 17, 27
        )
        ;

        UPDATE team
        SET division_id = 7
        WHERE team_id IN (
            0, 24, 25, 26
        )
        ;
    """)
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
