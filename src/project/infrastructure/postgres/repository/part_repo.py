from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.parts import PartsSchema, PartsCreateSchema
from project.infrastructure.postgres.models import Parts
from project.core.config import settings


class PartRepository:
    _collection: Type[Parts] = Parts
    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_parts(self, session: AsyncSession) -> list[PartsSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.parts_list;"
        result = await session.execute(text(query))
        return [PartsSchema.model_validate(obj=part) for part in result.mappings().all()]

    async def add_part(self, part: PartsCreateSchema, session: AsyncSession) -> PartsSchema:
        new_part = self._collection(**part.dict())
        session.add(new_part)
        await session.commit()
        await session.refresh(new_part)
        return PartsSchema.model_validate(new_part)

    async def get_part_by_id(self, part_id: int, session: AsyncSession) -> PartsSchema:
        query = select(self._collection).where(self._collection.id == part_id)
        result = await session.execute(query)
        part = result.scalar_one_or_none()
        return PartsSchema.model_validate(part)

    async def delete_part(self, part_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == part_id)
        result = await session.execute(query)
        part = result.scalar_one_or_none()

        if part:
            await session.delete(part)
            await session.commit()
            return True
        return False
