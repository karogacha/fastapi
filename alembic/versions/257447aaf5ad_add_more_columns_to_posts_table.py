"""add more columns to posts table

Revision ID: 257447aaf5ad
Revises: 7a8d982b5d11
Create Date: 2023-10-16 19:45:12.111236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '257447aaf5ad'
down_revision: Union[str, None] = '7a8d982b5d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
