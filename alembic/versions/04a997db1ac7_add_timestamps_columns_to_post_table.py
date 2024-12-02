"""add_timestamps_columns_to_post_table

Revision ID: 04a997db1ac7
Revises: 2302da58bc36
Create Date: 2024-07-10 02:55:32.348963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04a997db1ac7'
down_revision: Union[str, None] = '2302da58bc36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'created_at')
    # ### end Alembic commands ###
