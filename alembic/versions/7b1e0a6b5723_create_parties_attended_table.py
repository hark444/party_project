"""Create parties_attended table

Revision ID: 7b1e0a6b5723
Revises: eabce295344c
Create Date: 2022-08-25 03:47:30.294223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7b1e0a6b5723"
down_revision = "eabce295344c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parties_attended",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("party_id", sa.BigInteger(), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["party_id"],
            ["party.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["account_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_parties_attended_id"), "parties_attended", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_parties_attended_id"), table_name="parties_attended")
    op.drop_table("parties_attended")
    # ### end Alembic commands ###
