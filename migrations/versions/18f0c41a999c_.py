"""empty message

Revision ID: 18f0c41a999c
Revises: ce6854c2952c
Create Date: 2024-07-11 17:36:54.972110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18f0c41a999c'
down_revision: Union[str, None] = 'ce6854c2952c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teachers', sa.Column('experience', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teachers', 'experience')
    # ### end Alembic commands ###
