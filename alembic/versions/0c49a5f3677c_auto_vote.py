"""auto-vote

Revision ID: 0c49a5f3677c
Revises: 97ee8900e0dd
Create Date: 2024-07-16 18:08:22.937506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c49a5f3677c'
down_revision: Union[str, None] = '97ee8900e0dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('ttile', sa.String(), nullable=False))
    op.drop_column('posts', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('posts', 'ttile')
    # ### end Alembic commands ###
