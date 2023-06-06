"""Removed approved field from parties attended

Revision ID: 83e536370a77
Revises: eaf6e1fb3ab5
Create Date: 2022-12-21 14:56:31.135304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "83e536370a77"
down_revision = "eaf6e1fb3ab5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("parties_attended", "approved")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "parties_attended",
        sa.Column("approved", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###
