"""add last few columns to posts table

Revision ID: 39e52f40f332
Revises: 7ae4c23900c1
Create Date: 2023-10-17 10:36:29.870159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39e52f40f332'
down_revision: Union[str, None] = '7ae4c23900c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column(
                      'published', 
                      sa.Boolean(),
                      nullable=False, 
                      server_default='1'))
    op.add_column('posts',
                  sa.Column(
                      'created_at', 
                      sa.DATETIME(timezone=True),
                      server_default=sa.text('SYSDATETIMEOFFSET()'), 
                      nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
