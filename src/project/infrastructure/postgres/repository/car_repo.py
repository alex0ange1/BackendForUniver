from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.cars import CarsSchema, CarsCreateSchema
from project.infrastructure.postgres.models import Cars

from project.core.config import settings


class CarRepository:
    _collection: Type[Cars] = Cars

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False


    async def get_all_cars(self, session: AsyncSession) -> list[CarsSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.cars_list;"
        clients = await session.execute(text(query))
        return [CarsSchema.model_validate(obj=client) for client in clients.mappings().all()]


    async def add_car(self, car: CarsCreateSchema, session: AsyncSession) -> CarsSchema:
        new_car = self._collection(**car.dict())
        session.add(new_car)
        await session.commit()
        await session.refresh(new_car)
        return CarsSchema.model_validate(new_car)

    async def delete_car(self, car_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == car_id)
        result = await session.execute(query)
        car = result.scalar_one_or_none()

        await session.delete(car)
        await session.commit()
        return True

    async def get_car_by_id(self, car_id: int, session: AsyncSession) -> CarsSchema:
        query = select(self._collection).where(self._collection.id == car_id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        return CarsSchema.model_validate(client)