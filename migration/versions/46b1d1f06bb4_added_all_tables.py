"""Added all tables

Revision ID: 46b1d1f06bb4
Revises: de90de049862
Create Date: 2024-11-05 22:15:30.969798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from project.core.config import settings

revision: str = '46b1d1f06bb4'
down_revision: Union[str, None] = 'de90de049862'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS my_app_schema")
    op.create_table('cars_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('make_and_model', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('sts', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('year_of_issue', sa.Integer(), nullable=False),
    sa.Column('engine_displacement', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sts'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('parts_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('country_of_manufacture', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('purchase_price', sa.Integer(), nullable=False),
    sa.Column('selling_price', sa.Integer(), nullable=False, unique=True),
    sa.Column('status', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('quantity_in_stock', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('workers_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('salary', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='my_app_schema'
    )
    op.create_table('cars_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('car_sts', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('cost_of_provided_services', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_sts'], ['my_app_schema.cars_list.sts'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['my_app_schema.clients_list.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('parts_for_car',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['my_app_schema.cars_list.id'], ),
    sa.ForeignKeyConstraint(['part_id'], ['my_app_schema.parts_list.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('service_cost', sa.Integer(), nullable=False, unique=True),
    sa.Column('part_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['part_id'], ['my_app_schema.parts_list.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('receipt',
    sa.Column('service_receipt_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('car_sts', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('date', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_sts'], ['my_app_schema.cars_list.sts'], ),
    sa.ForeignKeyConstraint(['client_id'], ['my_app_schema.clients_list.id'], ),
    sa.PrimaryKeyConstraint('service_receipt_id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('service_receipt',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=False),
    sa.Column('quantity_of_parts', sa.Integer(), nullable=False),
    sa.Column('part_cost', sa.Integer(), nullable=False),
    sa.Column('selling_cost', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['part_cost'], ['my_app_schema.parts_list.selling_price'], ),
    sa.ForeignKeyConstraint(['part_id'], ['my_app_schema.parts_list.id'], ),
    sa.ForeignKeyConstraint(['selling_cost'], ['my_app_schema.service.service_cost'], ),
    sa.ForeignKeyConstraint(['service_id'], ['my_app_schema.service.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('workers_able_to_provide_service',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['my_app_schema.service.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['my_app_schema.workers_list.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )


def downgrade() -> None:
    op.drop_table('workers_able_to_provide_service', schema='my_app_schema')
    op.drop_table('service_receipt', schema='my_app_schema')
    op.drop_table('receipt', schema='my_app_schema')
    op.drop_table('service', schema='my_app_schema')
    op.drop_table('parts_for_car', schema='my_app_schema')
    op.drop_table('cars_status', schema='my_app_schema')
    op.drop_table('workers_list', schema='my_app_schema')
    op.drop_table('parts_list', schema='my_app_schema')
    op.drop_table('clients_list', schema='my_app_schema')
    op.drop_table('cars_list', schema='my_app_schema')
