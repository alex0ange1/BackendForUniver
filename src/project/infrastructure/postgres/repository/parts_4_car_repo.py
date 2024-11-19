from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.parts_for_car import PartsForCarSchema, PartsForCarCreateSchema
from project.infrastructure.postgres.models import PartsForCar
from project.core.config import settings


class PartsForCarRepository:
    _collection: Type[PartsForCar] = PartsForCar
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_parts_for_car(self, session: AsyncSession) -> list[PartsForCarSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.parts_for_car;"
        result = await session.execute(text(query))
        return [PartsForCarSchema.model_validate(obj=part) for part in result.mappings().all()]

    async def add_part_for_car(self, part_for_car: PartsForCarCreateSchema, session: AsyncSession) -> PartsForCarSchema:
        new_part_for_car = self._collection(**part_for_car.dict())
        session.add(new_part_for_car)
        await session.commit()
        await session.refresh(new_part_for_car)
        return PartsForCarSchema.model_validate(new_part_for_car)

    async def get_part_for_car_by_id(self, part_for_car_id: int, session: AsyncSession) -> PartsForCarSchema:
        query = select(self._collection).where(self._collection.id == part_for_car_id)
        result = await session.execute(query)
        part_for_car = result.scalar_one_or_none()
        return PartsForCarSchema.model_validate(part_for_car)

    async def delete_part_for_car(self, part_for_car_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == part_for_car_id)
        result = await session.execute(query)
        part_for_car = result.scalar_one_or_none()

        if part_for_car:
            await session.delete(part_for_car)
            await session.commit()
            return True
        return False
