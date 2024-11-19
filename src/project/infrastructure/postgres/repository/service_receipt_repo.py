from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.service_receipts import ServiceReceiptSchema, ServiceReceiptCreateSchema
from project.infrastructure.postgres.models import ServiceReceipt
from project.core.config import settings


class ServiceReceiptRepository:
    _collection: Type[ServiceReceipt] = ServiceReceipt
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_service_receipts(self, session: AsyncSession) -> list[ServiceReceiptSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.service_receipt;"
        result = await session.execute(text(query))
        return [ServiceReceiptSchema.model_validate(obj=sr) for sr in result.mappings().all()]

    async def add_service_receipt(self, service_receipt: ServiceReceiptCreateSchema, session: AsyncSession) -> ServiceReceiptSchema:
        new_service_receipt = self._collection(**service_receipt.dict())
        session.add(new_service_receipt)
        await session.commit()
        await session.refresh(new_service_receipt)
        return ServiceReceiptSchema.model_validate(new_service_receipt)

    async def get_service_receipt_by_id(self, service_receipt_id: int, session: AsyncSession) -> ServiceReceiptSchema:
        query = select(self._collection).where(self._collection.id == service_receipt_id)
        result = await session.execute(query)
        service_receipt = result.scalar_one_or_none()
        return ServiceReceiptSchema.model_validate(service_receipt)

    async def delete_service_receipt(self, service_receipt_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == service_receipt_id)
        result = await session.execute(query)
        service_receipt = result.scalar_one_or_none()

        if service_receipt:
            await session.delete(service_receipt)
            await session.commit()
            return True
        return False
