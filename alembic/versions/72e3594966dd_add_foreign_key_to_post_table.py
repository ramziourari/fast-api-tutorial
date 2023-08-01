"""add foreign key to post table

Revision ID: 72e3594966dd
Revises: b608e5fb0569
Create Date: 2023-08-01 14:57:26.423691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "72e3594966dd"
down_revision = "b608e5fb0569"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
