from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

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
