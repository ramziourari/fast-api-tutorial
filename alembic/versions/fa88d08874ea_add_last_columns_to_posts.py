"""add last columns to posts

Revision ID: fa88d08874ea
Revises: 72e3594966dd
Create Date: 2023-08-01 15:04:24.355677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fa88d08874ea"
down_revision = "72e3594966dd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="True"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", column_name="published")
    op.drop_column("posts", column_name="created_at")
