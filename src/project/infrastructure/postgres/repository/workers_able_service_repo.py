from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.worker_able_service import (
    WorkersAbleToProvideServiceSchema,
    WorkersAbleToProvideServiceCreateSchema,
)
from project.infrastructure.postgres.models import WorkersAbleToProvideService
from project.core.config import settings


class WorkersAbleToProvideServiceRepository:
    _collection: Type[WorkersAbleToProvideService] = WorkersAbleToProvideService
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_workers_services(self, session: AsyncSession) -> list[WorkersAbleToProvideServiceSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.workers_able_to_provide_service;"
        result = await session.execute(text(query))
        return [WorkersAbleToProvideServiceSchema.model_validate(obj=ws) for ws in result.mappings().all()]

    async def add_worker_service(self, ws: WorkersAbleToProvideServiceCreateSchema, session: AsyncSession) -> WorkersAbleToProvideServiceSchema:
        new_ws = self._collection(**ws.dict())
        session.add(new_ws)
        await session.commit()
        await session.refresh(new_ws)
        return WorkersAbleToProvideServiceSchema.model_validate(new_ws)

    async def get_worker_service_by_id(self, ws_id: int, session: AsyncSession) -> WorkersAbleToProvideServiceSchema:
        query = select(self._collection).where(self._collection.id == ws_id)
        result = await session.execute(query)
        ws = result.scalar_one_or_none()
        return WorkersAbleToProvideServiceSchema.model_validate(ws)

    async def delete_worker_service(self, ws_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == ws_id)
        result = await session.execute(query)
        ws = result.scalar_one_or_none()

        if ws:
            await session.delete(ws)
            await session.commit()
            return True
        return False
