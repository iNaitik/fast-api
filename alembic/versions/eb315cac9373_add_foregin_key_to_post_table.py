"""add foregin key to post table

Revision ID: eb315cac9373
Revises: 5d6e0494abad
Create Date: 2026-06-14 20:37:33.432685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb315cac9373'
down_revision: Union[str, Sequence[str], None] = '5d6e0494abad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", 
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
