import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.detailed_order import ReceiptDetailsSchema
from project.schemas.receipts import ReceiptSchema, ReceiptCreateSchema
from project.infrastructure.postgres.models import Receipt
from project.core.config import settings


class ReceiptRepository:
    _collection: Type[Receipt] = Receipt
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_receipts(self, session: AsyncSession) -> list[ReceiptSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.receipt;"
        result = await session.execute(text(query))
        return [ReceiptSchema.model_validate(obj=receipt) for receipt in result.mappings().all()]

    async def add_receipt(self, receipt: ReceiptCreateSchema, session: AsyncSession) -> ReceiptSchema:
        new_receipt = self._collection(**receipt.dict())
        session.add(new_receipt)
        await session.commit()
        await session.refresh(new_receipt)
        return ReceiptSchema.model_validate(new_receipt)

    async def get_receipt_by_id(self, receipt_id: int, session: AsyncSession) -> ReceiptSchema:
        query = select(self._collection).where(self._collection.service_receipt_id == receipt_id)
        result = await session.execute(query)
        receipt = result.scalar_one_or_none()
        return ReceiptSchema.model_validate(receipt)

    async def delete_receipt(self, receipt_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.service_receipt_id == receipt_id)
        result = await session.execute(query)
        receipt = result.scalar_one_or_none()

        if receipt:
            await session.delete(receipt)
            await session.commit()
            return True
        return False

    async def get_all_receipts(session: AsyncSession) -> list[ReceiptDetailsSchema]:
        query = text("""
            SELECT
                "receipt"."id" AS receipt_id,
                "receipt"."date" AS receipt_date,
                ("service"."service_cost" + "parts_list"."selling_price") AS total_cost,
                "clients_list"."full_name" AS client_name,
                "cars_list"."make_and_model" AS car_model,
                "cars_list"."sts" AS car_sts,
                "service"."name" AS service_name,
                "service"."service_cost" AS service_cost,
                "parts_list"."name" AS part_name,
                "parts_list"."selling_price" AS part_selling_price
            FROM "receipt"
            JOIN "clients_list" ON "receipt"."client_id" = "clients_list"."id"
            JOIN "cars_list" ON "receipt"."car_id" = "cars_list"."id"
            JOIN "service_receipt" ON "receipt"."service_receipt_id" = "service_receipt"."id"
            JOIN "service" ON "service_receipt"."service_id" = "service"."id"
            JOIN "parts_list" ON "service_receipt"."part_id" = "parts_list"."id";
        """)

        result = await session.execute(query)
        detailed_receipts = result.mappings().all()

        return [
            ReceiptDetailsSchema(**receipt) for receipt in detailed_receipts
        ]

    async def get_receipts_by_client_id(session: AsyncSession, client_id: int) -> list[ReceiptDetailsSchema]:
        query = text("""
            SELECT
                my_app_schema.receipt.id AS receipt_id,
                receipt.date AS receipt_date,
                (service.service_cost + parts_list.selling_price) AS total_cost,
                clients_list.full_name AS client_name,
                cars_list.make_and_model AS car_model,
                cars_list.sts AS car_sts,
                service.name AS service_name,
                service.service_cost AS service_cost,
                parts_list.name AS part_name,
                parts_list.selling_price AS part_selling_price
            FROM my_app_schema.receipt
            JOIN my_app_schema.clients_list ON receipt.client_id = clients_list.id
            JOIN my_app_schema.cars_list ON receipt.car_id = cars_list.id
            JOIN my_app_schema.service_receipt ON receipt.service_receipt_id = service_receipt.id
            JOIN my_app_schema.service ON service_receipt.service_id = service.id
            JOIN my_app_schema.parts_list ON service_receipt.part_id = parts_list.id
            WHERE receipt.client_id = :client_id
            ORDER BY my_app_schema.receipt.date ASC;
        """)

        result = await session.execute(query, {"client_id": client_id})
        detailed_receipts = result.mappings().all()

        return [
            ReceiptDetailsSchema(**receipt) for receipt in detailed_receipts
        ]

    async def get_receipts_by_date_range(session: AsyncSession, start_date: datetime.date, end_date: datetime.date) -> list[
        ReceiptDetailsSchema]:
        query = text("""
                    SELECT
                        my_app_schema.receipt.id AS receipt_id,
                        my_app_schema.receipt.date AS receipt_date,
                        (my_app_schema.service.service_cost + my_app_schema.parts_list.selling_price) AS total_cost,
                        my_app_schema.clients_list.full_name AS client_name,
                        my_app_schema.cars_list.make_and_model AS car_model,
                        my_app_schema.cars_list.sts AS car_sts,
                        my_app_schema.service.name AS service_name,
                        my_app_schema.service.service_cost AS service_cost,
                        my_app_schema.parts_list.name AS part_name,
                        my_app_schema.parts_list.selling_price AS part_selling_price
                    FROM my_app_schema.receipt
                    JOIN my_app_schema.clients_list ON my_app_schema.receipt.client_id = my_app_schema.clients_list.id
                    JOIN my_app_schema.cars_list ON my_app_schema.receipt.car_id = my_app_schema.cars_list.id
                    JOIN my_app_schema.service_receipt ON my_app_schema.receipt.service_receipt_id = my_app_schema.service_receipt.id
                    JOIN my_app_schema.service ON my_app_schema.service_receipt.service_id = my_app_schema.service.id
                    JOIN my_app_schema.parts_list ON my_app_schema.service_receipt.part_id = my_app_schema.parts_list.id
                    WHERE my_app_schema.receipt.date BETWEEN :start_date AND :end_date
                    ORDER BY my_app_schema.receipt.date ASC;
                """)

        result = await session.execute(query, {"start_date": start_date, "end_date": end_date})
        detailed_receipts = result.mappings().all()

        return [
            ReceiptDetailsSchema(**receipt) for receipt in detailed_receipts
        ]

    async def get_receipts_by_date_range_and_client(session: AsyncSession, start_date: datetime.date, end_date: datetime.date,
                                                    client_id: int) -> list[ReceiptDetailsSchema]:
        query = text("""
                            SELECT
                                my_app_schema.receipt.id AS receipt_id,
                                my_app_schema.receipt.date AS receipt_date,
                                (my_app_schema.service.service_cost + my_app_schema.parts_list.selling_price) AS total_cost,
                                my_app_schema.clients_list.full_name AS client_name,
                                my_app_schema.cars_list.make_and_model AS car_model,
                                my_app_schema.cars_list.sts AS car_sts,
                                my_app_schema.service.name AS service_name,
                                my_app_schema.service.service_cost AS service_cost,
                                my_app_schema.parts_list.name AS part_name,
                                my_app_schema.parts_list.selling_price AS part_selling_price
                            FROM my_app_schema.receipt
                            JOIN my_app_schema.clients_list ON my_app_schema.receipt.client_id = my_app_schema.clients_list.id
                            JOIN my_app_schema.cars_list ON my_app_schema.receipt.car_id = my_app_schema.cars_list.id
                            JOIN my_app_schema.service_receipt ON my_app_schema.receipt.service_receipt_id = my_app_schema.service_receipt.id
                            JOIN my_app_schema.service ON my_app_schema.service_receipt.service_id = my_app_schema.service.id
                            JOIN my_app_schema.parts_list ON my_app_schema.service_receipt.part_id = my_app_schema.parts_list.id
                            WHERE my_app_schema.receipt.client_id = :client_id
                              AND my_app_schema.receipt.date BETWEEN :start_date AND :end_date
                            ORDER BY my_app_schema.receipt.date ASC;
                        """)

        result = await session.execute(query, {
            "start_date": start_date,
            "end_date": end_date,
            "client_id": client_id
        })
        detailed_receipts = result.mappings().all()

        return [
            ReceiptDetailsSchema(**receipt) for receipt in detailed_receipts
        ]


