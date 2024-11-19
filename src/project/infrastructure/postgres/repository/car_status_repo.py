from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.cars_status import CarsStatusSchema, CarsStatusCreateSchema
from project.infrastructure.postgres.models import CarsStatus
from project.core.config import settings

class CarsStatusRepository:
    _collection: Type[CarsStatus] = CarsStatus

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False


    async def get_all_cars_status(self, session: AsyncSession) -> list[CarsStatusSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.cars_status;"
        result = await session.execute(text(query))
        return [CarsStatusSchema.model_validate(obj=status) for status in result.mappings().all()]

    async def add_cars_status(self, car_status: CarsStatusCreateSchema, session: AsyncSession) -> CarsStatusSchema:
        new_status = self._collection(**car_status.dict())
        session.add(new_status)
        await session.commit()
        await session.refresh(new_status)
        return CarsStatusSchema.model_validate(new_status)

    async def get_cars_status_by_id(self, status_id: int, session: AsyncSession) -> CarsStatusSchema:
        query = select(self._collection).where(self._collection.id == status_id)
        result = await session.execute(query)
        status = result.scalar_one_or_none()
        return CarsStatusSchema.model_validate(status)

    async def delete_cars_status(self, status_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == status_id)
        result = await session.execute(query)
        status = result.scalar_one_or_none()

        if status:
            await session.delete(status)
            await session.commit()
            return True
        return False
