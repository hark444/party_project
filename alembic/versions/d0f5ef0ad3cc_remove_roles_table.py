"""remove roles table

Revision ID: d0f5ef0ad3cc
Revises: 5b2fc697ff0d
Create Date: 2023-03-03 20:54:21.587365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d0f5ef0ad3cc"
down_revision = "5b2fc697ff0d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_roles_id", table_name="roles")
    op.drop_table("roles")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "roles",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="roles_pkey"),
        sa.UniqueConstraint("role", name="roles_role_key"),
    )
    op.create_index("ix_roles_id", "roles", ["id"], unique=False)
    # ### end Alembic commands ###