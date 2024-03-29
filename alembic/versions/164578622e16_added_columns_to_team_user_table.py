"""added columns to team user table

Revision ID: 164578622e16
Revises: 212c0582bf6a
Create Date: 2023-02-28 19:27:29.021575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "164578622e16"
down_revision = "212c0582bf6a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "team_user", sa.Column("requested_by_id", sa.Integer(), nullable=True)
    )
    op.add_column("team_user", sa.Column("team_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None, "team_user", "account_user", ["requested_by_id"], ["id"]
    )
    op.create_foreign_key(None, "team_user", "teams", ["team_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "team_user", type_="foreignkey")
    op.drop_constraint(None, "team_user", type_="foreignkey")
    op.drop_column("team_user", "team_id")
    op.drop_column("team_user", "requested_by_id")
    # ### end Alembic commands ###
