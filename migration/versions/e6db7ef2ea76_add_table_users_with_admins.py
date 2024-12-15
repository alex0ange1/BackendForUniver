"""add_table_users_with_admins

Revision ID: e6db7ef2ea76
Revises: 46b1d1f06bb4
Create Date: 2024-12-13 21:55:04.474095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6db7ef2ea76'
down_revision: Union[str, None] = '46b1d1f06bb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('last_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('email', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('password', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('phone_number', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='my_app_schema'
    )



def downgrade() -> None:
    op.drop_table('users', schema='my_app_schema')
