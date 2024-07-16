# this file is creating using the command alembic revision -m create posts table and its resposable for creating a post table


"""create posts table

Revision ID: 15eb06db5da6
Revises: 
Create Date: 2024-07-15 22:17:43.689464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15eb06db5da6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# creating the columns for Post table. the information on alembic.sqlalchemy.org - ddl
def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass

#to delete the table
def downgrade():
    op.drop_table('posts')
    pass
