"""fixed all the columns

Revision ID: dec874ccc3a9
Revises: 8f54227d7102
Create Date: 2024-12-19 23:19:38.304932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dec874ccc3a9'
down_revision: Union[str, None] = '8f54227d7102'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_car_sts', 'cars_status', ['car_sts'], schema='my_app_schema')
    op.create_unique_constraint('uq_owner_id', 'cars_status', ['owner_id'], schema='my_app_schema')
    op.create_unique_constraint(None, 'parts_list', ['id'], schema='my_app_schema')
    op.add_column('receipt', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False), schema='my_app_schema')
    op.add_column('receipt', sa.Column('car_id', sa.Integer(), nullable=False), schema='my_app_schema')
    op.alter_column('receipt', 'date',
               existing_type=sa.INTEGER(),
               type_=sa.Date(),
               existing_nullable=False,
               schema='my_app_schema')
    op.drop_constraint('receipt_car_sts_fkey', 'receipt', schema='my_app_schema', type_='foreignkey')
    op.create_foreign_key(None, 'receipt', 'service_receipt', ['service_receipt_id'], ['id'], source_schema='my_app_schema', referent_schema='my_app_schema')
    op.create_foreign_key(None, 'receipt', 'cars_list', ['car_id'], ['id'], source_schema='my_app_schema', referent_schema='my_app_schema')
    op.drop_column('receipt', 'car_sts', schema='my_app_schema')
    op.create_unique_constraint(None, 'service', ['id'], schema='my_app_schema')
    op.drop_constraint('service_receipt_selling_cost_fkey', 'service_receipt', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint('service_receipt_part_cost_fkey', 'service_receipt', schema='my_app_schema', type_='foreignkey')
    op.drop_column('service_receipt', 'part_cost', schema='my_app_schema')
    op.drop_column('service_receipt', 'quantity_of_parts', schema='my_app_schema')
    op.drop_column('service_receipt', 'selling_cost', schema='my_app_schema')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_receipt', sa.Column('selling_cost', sa.INTEGER(), autoincrement=False, nullable=False), schema='my_app_schema')
    op.add_column('service_receipt', sa.Column('quantity_of_parts', sa.INTEGER(), autoincrement=False, nullable=False), schema='my_app_schema')
    op.add_column('service_receipt', sa.Column('part_cost', sa.INTEGER(), autoincrement=False, nullable=False), schema='my_app_schema')
    op.create_foreign_key('service_receipt_part_cost_fkey', 'service_receipt', 'parts_list', ['part_cost'], ['selling_price'], source_schema='my_app_schema', referent_schema='my_app_schema')
    op.create_foreign_key('service_receipt_selling_cost_fkey', 'service_receipt', 'service', ['selling_cost'], ['service_cost'], source_schema='my_app_schema', referent_schema='my_app_schema')
    op.drop_constraint(None, 'service', schema='my_app_schema', type_='unique')
    op.add_column('receipt', sa.Column('car_sts', sa.VARCHAR(length=255), autoincrement=False, nullable=False), schema='my_app_schema')
    op.drop_constraint(None, 'receipt', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'receipt', schema='my_app_schema', type_='foreignkey')
    op.create_foreign_key('receipt_car_sts_fkey', 'receipt', 'cars_list', ['car_sts'], ['sts'], source_schema='my_app_schema', referent_schema='my_app_schema')
    op.alter_column('receipt', 'date',
               existing_type=sa.Date(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               schema='my_app_schema')
    op.drop_column('receipt', 'car_id', schema='my_app_schema')
    op.drop_column('receipt', 'id', schema='my_app_schema')
    op.drop_constraint(None, 'parts_list', schema='my_app_schema', type_='unique')
    op.drop_constraint('uq_owner_id', 'cars_status', schema='my_app_schema', type_='unique')
    op.drop_constraint('uq_car_sts', 'cars_status', schema='my_app_schema', type_='unique')
    # ### end Alembic commands ###