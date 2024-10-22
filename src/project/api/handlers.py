from fastapi import APIRouter, HTTPException
from src.project.infrastructure.postgres.repository.user_repo import UserRepository
from src.project.infrastructure.postgres.database import PostgresDatabase
from src.project.schemas.clients import ClientsSchema, ClientCreateSchema

router = APIRouter()


@router.get("/all_clients", response_model=list[ClientsSchema])
async def get_all_clients() -> list[ClientsSchema]:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_clients = await user_repo.get_all_clients(session=session)

    return all_clients


@router.get("/client/{client_id}", response_model=ClientsSchema)
async def get_client_by_id(client_id: int) -> ClientsSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        user = await user_repo.get_client_by_id(client_id=client_id, session=session)

        if user is None:
            raise HTTPException(status_code=404, detail="User  not found")

    return user


@router.post("/add_client", response_model=ClientsSchema)
async def add_client(client: ClientCreateSchema) -> ClientsSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        new_client = await user_repo.add_client(client=client, session=session)

    return new_client


@router.delete("/delete_client/{client_id}", response_model=dict)
async def delete_client(client_id: int) -> dict:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        deleted = await user_repo.delete_client(client_id=client_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Client not found")

    return {"detail": "Client deleted successfully"}