"""added field date_of_birth in table Users

Revision ID: 8f54227d7102
Revises: e6db7ef2ea76
Create Date: 2024-12-13 22:09:25.596533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f54227d7102'
down_revision: Union[str, None] = 'e6db7ef2ea76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=False), schema='my_app_schema')


def downgrade() -> None:
    op.drop_column('users', 'date_of_birth', schema='my_app_schema')