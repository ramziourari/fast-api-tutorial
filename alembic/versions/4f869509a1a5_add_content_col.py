"""add content col

Revision ID: 4f869509a1a5
Revises: 3469b3479a22
Create Date: 2023-08-01 14:27:51.804313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4f869509a1a5"
down_revision = "3469b3479a22"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
