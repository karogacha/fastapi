"""create posts table

Revision ID: 7a8d982b5d11
Revises: 
Create Date: 2023-10-16 19:37:55.497822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a8d982b5d11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column(
                        'id',
                        sa.Integer(),
                        nullable=False, 
                        primary_key=True
                        ),
                        sa.Column(
                            'title', 
                            sa.String(),
                            nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
