"""populate permissions table

Revision ID: 305570004339
Revises: 53e16ac8b0f5
Create Date: 2023-02-22 23:29:49.747888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "305570004339"
down_revision = "53e16ac8b0f5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("insert into permissions values (DEFAULT, 'create_admin')")
    op.execute("insert into permissions values (DEFAULT, 'add_user_to_team')")
    op.execute("insert into permissions values (DEFAULT, 'remove_user_from_team')")
    op.execute("insert into permissions values (DEFAULT, 'send_email')")
    op.execute("insert into permissions values (DEFAULT, 'create_party')")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute(
        "delete from permissions where permission in ('create_admin', 'add_user_to_team', 'remove_user_from_team', 'send_email', 'create_party')"
    )
    # ### end Alembic commands ###
