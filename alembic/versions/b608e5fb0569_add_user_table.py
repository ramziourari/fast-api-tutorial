"""add user table

Revision ID: b608e5fb0569
Revises: 4f869509a1a5
Create Date: 2023-08-01 14:33:06.336554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b608e5fb0569"
down_revision = "4f869509a1a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
