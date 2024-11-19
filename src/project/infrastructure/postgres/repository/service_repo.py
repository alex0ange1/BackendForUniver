from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.services import ServiceSchema, ServiceCreateSchema
from project.infrastructure.postgres.models import Service
from project.core.config import settings


class ServiceRepository:
    _collection: Type[Service] = Service
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_services(self, session: AsyncSession) -> list[ServiceSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.service;"
        result = await session.execute(text(query))
        return [ServiceSchema.model_validate(obj=service) for service in result.mappings().all()]

    async def add_service(self, service: ServiceCreateSchema, session: AsyncSession) -> ServiceSchema:
        new_service = self._collection(**service.dict())
        session.add(new_service)
        await session.commit()
        await session.refresh(new_service)
        return ServiceSchema.model_validate(new_service)

    async def get_service_by_id(self, service_id: int, session: AsyncSession) -> ServiceSchema:
        query = select(self._collection).where(self._collection.id == service_id)
        result = await session.execute(query)
        service = result.scalar_one_or_none()
        return ServiceSchema.model_validate(service)

    async def delete_service(self, service_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == service_id)
        result = await session.execute(query)
        service = result.scalar_one_or_none()

        if service:
            await session.delete(service)
            await session.commit()
            return True
        return False
