"""deleted table receipt

Revision ID: f7f412104828
Revises: dec874ccc3a9
Create Date: 2024-12-20 00:09:59.995149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7f412104828'
down_revision: Union[str, None] = 'dec874ccc3a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем таблицу receipt
    op.drop_table('receipt', schema='my_app_schema')

    # Создаем таблицу receipt заново
    op.create_table(
        'receipt',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('client_id', sa.Integer(), sa.ForeignKey('my_app_schema.clients_list.id'), nullable=False),
        sa.Column('service_receipt_id', sa.Integer(), sa.ForeignKey('my_app_schema.service_receipt.id'),
                  nullable=False),
        sa.Column('car_id', sa.Integer(), sa.ForeignKey('my_app_schema.cars_list.id'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=False),
        schema='my_app_schema'
    )

    sa.ForeignKeyConstraint(['client_id'], ['my_app_schema.clients_list.id'], )
    sa.ForeignKeyConstraint(['service_receipt_id'], ['my_app_schema.service_receipt.id'], )
    sa.ForeignKeyConstraint(['car_id'], ['my_app_schema.cars_list.id'], )


def downgrade() -> None:
    # Восстанавливаем таблицу receipt с её старой структурой (если необходимо)
    op.create_table(
        'receipt',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('client_id', sa.Integer(), sa.ForeignKey('my_app_schema.clients_list.id'), nullable=False),
        sa.Column('service_receipt_id', sa.Integer(), sa.ForeignKey('my_app_schema.service_receipt.id'),
                  nullable=False),
        sa.Column('car_sts', sa.String(length=255), nullable=False),  # возвращаем car_sts
        sa.Column('date', sa.Integer(), nullable=False),  # изменяем тип обратно
        sa.Column('cost', sa.Integer(), nullable=False),
        schema='my_app_schema'
    )

