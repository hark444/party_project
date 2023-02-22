"""populate roles table

Revision ID: 53e16ac8b0f5
Revises: 683567424c0f
Create Date: 2023-02-22 23:03:05.376565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "53e16ac8b0f5"
down_revision = "683567424c0f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("insert into roles values (DEFAULT, 'superuser')")
    op.execute("insert into roles values (DEFAULT, 'admin')")
    op.execute("insert into roles values (DEFAULT, 'regular')")

    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("delete from roles where role in ('superuser', 'admin', 'regular')")
    # ### end Alembic commands ###
