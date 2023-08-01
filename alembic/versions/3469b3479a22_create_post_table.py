"""create post table

Revision ID: 3469b3479a22
Revises: 
Create Date: 2023-08-01 14:02:15.770031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3469b3479a22"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.INTEGER(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
