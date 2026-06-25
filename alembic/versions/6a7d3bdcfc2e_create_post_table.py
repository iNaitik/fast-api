"""create post table

Revision ID: 6a7d3bdcfc2e
Revises: 
Create Date: 2026-06-14 20:12:25.520292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a7d3bdcfc2e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Upgrade Function: This function is used to upgrade the database schema to the new version.
# In this function, we will create the posts table in the database using the 
# SQLAlchemy's op.create_table() function. 
# We will define the columns of the table and their data types, and also specify the 
# primary key and foreign key constraints.
def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("published", sa.Boolean, server_default='TRUE', nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    )


# Downgrade Function: This function is used to downgrade the database schema to the previous version.
# In this function, we will drop the posts table from the database using the 
# SQLAlchemy's op.drop_table() function. 
# This will remove the posts table from the database and all the data stored in it, 
# so we should be careful while running this function.
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
