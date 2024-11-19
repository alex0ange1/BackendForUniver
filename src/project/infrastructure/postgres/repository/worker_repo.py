from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.workers import WorkersSchema, WorkersCreateSchema
from project.infrastructure.postgres.models import Workers
from project.core.config import settings


class WorkerRepository:
    _collection: Type[Workers] = Workers
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_workers(self, session: AsyncSession) -> list[WorkersSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.workers_list;"
        result = await session.execute(text(query))
        return [WorkersSchema.model_validate(obj=worker) for worker in result.mappings().all()]

    async def add_worker(self, worker: WorkersCreateSchema, session: AsyncSession) -> WorkersSchema:
        new_worker = self._collection(**worker.dict())
        session.add(new_worker)
        await session.commit()
        await session.refresh(new_worker)
        return WorkersSchema.model_validate(new_worker)

    async def get_worker_by_id(self, worker_id: int, session: AsyncSession) -> WorkersSchema:
        query = select(self._collection).where(self._collection.id == worker_id)
        result = await session.execute(query)
        worker = result.scalar_one_or_none()
        return WorkersSchema.model_validate(worker)

    async def delete_worker(self, worker_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == worker_id)
        result = await session.execute(query)
        worker = result.scalar_one_or_none()

        if worker:
            await session.delete(worker)
            await session.commit()
            return True
        return False
