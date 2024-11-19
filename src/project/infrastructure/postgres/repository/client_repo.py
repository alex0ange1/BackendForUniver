from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.clients import ClientsSchema, ClientCreateSchema
from project.infrastructure.postgres.models import Clients

from project.core.config import settings


class ClientRepository:
    _collection: Type[Clients] = Clients

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False


    async def get_all_clients(self, session: AsyncSession) -> list[ClientsSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.clients_list;"
        clients = await session.execute(text(query))
        return [ClientsSchema.model_validate(obj=client) for client in clients.mappings().all()]


    async def add_client(self, client: ClientCreateSchema, session: AsyncSession) -> ClientsSchema:
        new_client = self._collection(**client.dict())
        session.add(new_client)
        await session.commit()
        await session.refresh(new_client)
        return ClientsSchema.model_validate(new_client)

    async def delete_client(self, client_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == client_id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        await session.delete(client)
        await session.commit()
        return True

    async def get_client_by_id(self, client_id: int, session: AsyncSession) -> ClientsSchema:
        query = select(self._collection).where(self._collection.id == client_id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        return ClientsSchema.model_validate(client)