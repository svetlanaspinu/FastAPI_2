"""add content column to posts table

Revision ID: d70e8f6aa033
Revises: 15eb06db5da6
Create Date: 2024-07-15 22:37:11.210419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd70e8f6aa033'
down_revision: Union[str, None] = '15eb06db5da6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
