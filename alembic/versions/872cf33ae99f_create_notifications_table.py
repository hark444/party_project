"""create notifications table

Revision ID: 872cf33ae99f
Revises: ee3ddaef8ae0
Create Date: 2023-03-02 01:01:09.829349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "872cf33ae99f"
down_revision = "ee3ddaef8ae0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "type",
            sa.Enum(
                "OPT_IN",
                "OPT_OUT",
                "WELCOME",
                "LIKE",
                "COMMENT",
                "APPROVAL",
                "BIRTHDAY",
                name="notificationtypeenum",
            ),
            server_default="WELCOME",
            nullable=False,
        ),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("expired", sa.Boolean(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=False),
        sa.Column("last_modified_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["account_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notifications_id"), "notifications", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_notifications_id"), table_name="notifications")
    op.drop_table("notifications")
    # ### end Alembic commands ###
