"""Added roles to user

Revision ID: fe127e12017c
Revises: 538273900378
Create Date: 2022-08-21 02:46:04.854325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fe127e12017c"
down_revision = "538273900378"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE roletypeenum AS ENUM ('admin', 'superuser', 'regular')")
    op.add_column(
        "account_user",
        sa.Column(
            "role",
            sa.Enum("ADMIN", "SUPERUSER", "REGULAR", name="roletypeenum"),
            server_default="regular",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("account_user", "role")
    op.execute("DROP TYPE roletypeenum;")
    # ### end Alembic commands ###