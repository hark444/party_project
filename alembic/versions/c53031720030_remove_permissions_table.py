"""remove permissions table

Revision ID: c53031720030
Revises: e2af834ca291
Create Date: 2023-03-02 16:18:12.602974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c53031720030"
down_revision = "e2af834ca291"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_permissions_id", table_name="permissions")
    op.drop_table("permissions")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "permissions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("permission", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="permissions_pkey"),
        sa.UniqueConstraint("permission", name="permissions_permission_key"),
    )
    op.create_index("ix_permissions_id", "permissions", ["id"], unique=False)
    # ### end Alembic commands ###
