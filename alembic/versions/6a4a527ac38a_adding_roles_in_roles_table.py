"""Adding roles in roles table

Revision ID: 6a4a527ac38a
Revises: f922bf57da4c
Create Date: 2022-08-06 02:44:54.763582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a4a527ac38a'
down_revision = 'f922bf57da4c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("insert into roles values (1, 'superuser', false)")
    op.execute("insert into roles values (2, 'admin', false)")
    op.execute("insert into roles values (3, 'user', false)")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("delete from roles where id = 1")
    op.execute("delete from roles where id = 2")
    op.execute("delete from roles where id = 3")
    # ### end Alembic commands ###
