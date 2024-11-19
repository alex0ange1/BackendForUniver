from fastapi import APIRouter, HTTPException
from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.car_repo import CarRepository
from project.infrastructure.postgres.repository.part_repo import PartRepository
from project.infrastructure.postgres.repository.worker_repo import WorkerRepository
from project.infrastructure.postgres.repository.service_repo import ServiceRepository
from project.infrastructure.postgres.repository.car_status_repo import CarsStatusRepository
from project.infrastructure.postgres.repository.service_receipt_repo import ServiceReceiptRepository
from project.infrastructure.postgres.repository.parts_4_car_repo import PartsForCarRepository
from project.infrastructure.postgres.repository.receipt_repo import ReceiptRepository
from project.infrastructure.postgres.repository.workers_able_service_repo import WorkersAbleToProvideServiceRepository

from project.infrastructure.postgres.database import PostgresDatabase

from project.schemas.clients import ClientsSchema, ClientCreateSchema
from project.schemas.cars import CarsSchema, CarsCreateSchema
from project.schemas.parts import PartsSchema, PartsCreateSchema
from project.schemas.workers import WorkersSchema, WorkersCreateSchema
from project.schemas.services import ServiceSchema, ServiceCreateSchema
from project.schemas.cars_status import CarsStatusSchema, CarsStatusCreateSchema
from project.schemas.service_receipts import ServiceReceiptSchema, ServiceReceiptCreateSchema
from project.schemas.parts_for_car import PartsForCarSchema, PartsForCarCreateSchema
from project.schemas.receipts import ReceiptSchema, ReceiptCreateSchema
from project.schemas.worker_able_service \
    import WorkersAbleToProvideServiceSchema, WorkersAbleToProvideServiceCreateSchema

router = APIRouter()


@router.get("/all_clients", response_model=list[ClientsSchema])
async def get_all_clients() -> list[ClientsSchema]:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        all_clients = await client_repo.get_all_clients(session=session)

    return all_clients


@router.get("/client/{client_id}", response_model=ClientsSchema)
async def get_client_by_id(client_id: int) -> ClientsSchema:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        user = await client_repo.get_client_by_id(client_id=client_id, session=session)

        if user is None:
            raise HTTPException(status_code=404, detail="User  not found")

    return user


@router.post("/add_client", response_model=ClientsSchema)
async def add_client(client: ClientCreateSchema) -> ClientsSchema:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        new_client = await client_repo.add_client(client=client, session=session)

    return new_client


@router.delete("/delete_client/{client_id}", response_model=dict)
async def delete_client(client_id: int) -> dict:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        deleted = await client_repo.delete_client(client_id=client_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Client not found")

    return {"detail": "Client deleted successfully"}


@router.get("/all_cars", response_model=list[CarsSchema])
async def get_all_clients() -> list[CarsSchema]:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        all_cars = await car_repo.get_all_cars(session=session)

    return all_cars


@router.get("/car/{car_id}", response_model=CarsSchema)
async def get_car_by_id(car_id: int) -> CarsSchema:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        user = await car_repo.get_car_by_id(car_id=car_id, session=session)

        if user is None:
            raise HTTPException(status_code=404, detail="Car  not found")

    return user


@router.post("/add_car", response_model=CarsSchema)
async def add_client(car: CarsCreateSchema) -> CarsSchema:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        new_client = await car_repo.add_car(car=car, session=session)

    return new_client


@router.delete("/delete_car/{car_id}", response_model=dict)
async def delete_client(car_id: int) -> dict:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        deleted = await car_repo.delete_car(car_id=car_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Car not found")

    return {"detail": "Car deleted successfully"}

@router.get("/all_workers", response_model=list[WorkersSchema])
async def get_all_workers() -> list[WorkersSchema]:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        all_workers = await worker_repo.get_all_workers(session=session)

    return all_workers


@router.get("/worker/{worker_id}", response_model=WorkersSchema)
async def get_worker_by_id(worker_id: int) -> WorkersSchema:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        worker = await worker_repo.get_worker_by_id(worker_id=worker_id, session=session)

        if worker is None:
            raise HTTPException(status_code=404, detail="Worker not found")

    return worker


@router.post("/add_worker", response_model=WorkersSchema)
async def add_worker(worker: WorkersCreateSchema) -> WorkersSchema:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        new_worker = await worker_repo.add_worker(worker=worker, session=session)

    return new_worker

@router.get("/all_parts", response_model=list[PartsSchema])
async def get_all_parts() -> list[PartsSchema]:
    parts_repo = PartRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_repo.check_connection(session=session)
        all_parts = await parts_repo.get_all_parts(session=session)

    return all_parts


@router.get("/part/{part_id}", response_model=PartsSchema)
async def get_part_by_id(part_id: int) -> PartsSchema:
    parts_repo = PartRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_repo.check_connection(session=session)
        part = await parts_repo.get_part_by_id(part_id=part_id, session=session)

        if part is None:
            raise HTTPException(status_code=404, detail="Part not found")

    return part


@router.post("/add_part", response_model=PartsSchema)
async def add_part(part: PartsCreateSchema) -> PartsSchema:
    parts_repo = PartRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_repo.check_connection(session=session)
        new_part = await parts_repo.add_part(part=part, session=session)

    return new_part


@router.delete("/delete_part/{part_id}", response_model=dict)
async def delete_part(part_id: int) -> dict:
    parts_repo = PartRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_repo.check_connection(session=session)
        deleted = await parts_repo.delete_part(part_id=part_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Part not found")

    return {"detail": "Part deleted successfully"}


@router.get("/all_services", response_model=list[ServiceSchema])
async def get_all_services() -> list[ServiceSchema]:
    service_repo = ServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_repo.check_connection(session=session)
        all_services = await service_repo.get_all_services(session=session)

    return all_services


@router.get("/service/{service_id}", response_model=ServiceSchema)
async def get_service_by_id(service_id: int) -> ServiceSchema:
    service_repo = ServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_repo.check_connection(session=session)
        service = await service_repo.get_service_by_id(service_id=service_id, session=session)

        if service is None:
            raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.post("/add_service", response_model=ServiceSchema)
async def add_service(service: ServiceCreateSchema) -> ServiceSchema:
    service_repo = ServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_repo.check_connection(session=session)
        new_service = await service_repo.add_service(service=service, session=session)

    return new_service


@router.delete("/delete_service/{service_id}", response_model=dict)
async def delete_service(service_id: int) -> dict:
    service_repo = ServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_repo.check_connection(session=session)
        deleted = await service_repo.delete_service(service_id=service_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Service not found")

    return {"detail": "Service deleted successfully"}


@router.get("/all_cars_status", response_model=list[CarsStatusSchema])
async def get_all_cars_status() -> list[CarsStatusSchema]:
    cars_status_repo = CarsStatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cars_status_repo.check_connection(session=session)
        all_cars_status = await cars_status_repo.get_all_cars_status(session=session)

    return all_cars_status


@router.get("/car_status/{status_id}", response_model=CarsStatusSchema)
async def get_car_status_by_id(status_id: int) -> CarsStatusSchema:
    cars_status_repo = CarsStatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cars_status_repo.check_connection(session=session)
        car_status = await cars_status_repo.get_cars_status_by_id(status_id=status_id, session=session)

        if car_status is None:
            raise HTTPException(status_code=404, detail="Car status not found")

    return car_status


@router.post("/add_car_status", response_model=CarsStatusSchema)
async def add_car_status(car_status: CarsStatusCreateSchema) -> CarsStatusSchema:
    cars_status_repo = CarsStatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cars_status_repo.check_connection(session=session)
        new_car_status = await cars_status_repo.add_cars_status(car_status=car_status, session=session)

    return new_car_status


@router.delete("/delete_car_status/{status_id}", response_model=dict)
async def delete_car_status(status_id: int) -> dict:
    cars_status_repo = CarsStatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cars_status_repo.check_connection(session=session)
        deleted = await cars_status_repo.delete_cars_status(status_id=status_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Car status not found")

    return {"detail": "Car status deleted successfully"}


@router.get("/all_workers_able_to_provide_service", response_model=list[WorkersAbleToProvideServiceSchema])
async def get_all_workers_able_to_provide_service() -> list[WorkersAbleToProvideServiceSchema]:
    workers_able_repo = WorkersAbleToProvideServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await workers_able_repo.check_connection(session=session)
        all_workers_able = await workers_able_repo.get_all_workers_services(session=session)

    return all_workers_able


@router.get("/worker_able/{worker_able_id}", response_model=WorkersAbleToProvideServiceSchema)
async def get_worker_able_by_id(worker_able_id: int) -> WorkersAbleToProvideServiceSchema:
    workers_able_repo = WorkersAbleToProvideServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await workers_able_repo.check_connection(session=session)
        worker_able = await workers_able_repo.get_worker_service_by_id(ws_id=worker_able_id, session=session)

        if worker_able is None:
            raise HTTPException(status_code=404, detail="Worker ability to provide service not found")

    return worker_able


@router.post("/add_worker_able_to_provide_service", response_model=WorkersAbleToProvideServiceSchema)
async def add_worker_able_to_provide_service(worker_able: WorkersAbleToProvideServiceCreateSchema) -> WorkersAbleToProvideServiceSchema:
    workers_able_repo = WorkersAbleToProvideServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await workers_able_repo.check_connection(session=session)
        new_worker_able = await workers_able_repo.add_worker_service(ws=worker_able, session=session)

    return new_worker_able


@router.delete("/delete_worker_able_to_provide_service/{worker_able_id}", response_model=dict)
async def delete_worker_able_to_provide_service(worker_able_id: int) -> dict:
    workers_able_repo = WorkersAbleToProvideServiceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await workers_able_repo.check_connection(session=session)
        deleted = await workers_able_repo.delete_worker_service(ws_id=worker_able_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Worker ability to provide service not found")

    return {"detail": "Worker ability to provide service deleted successfully"}


@router.get("/all_parts_for_car", response_model=list[PartsForCarSchema])
async def get_all_parts_for_car() -> list[PartsForCarSchema]:
    parts_for_car_repo = PartsForCarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_for_car_repo.check_connection(session=session)
        all_parts_for_car = await parts_for_car_repo.get_all_parts_for_car(session=session)

    return all_parts_for_car


@router.get("/part_for_car/{part_for_car_id}", response_model=PartsForCarSchema)
async def get_part_for_car_by_id(part_for_car_id: int) -> PartsForCarSchema:
    parts_for_car_repo = PartsForCarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_for_car_repo.check_connection(session=session)
        part_for_car = await parts_for_car_repo.get_part_for_car_by_id(part_for_car_id=part_for_car_id, session=session)

        if part_for_car is None:
            raise HTTPException(status_code=404, detail="Part for car not found")

    return part_for_car


@router.post("/add_part_for_car", response_model=PartsForCarSchema)
async def add_part_for_car(part_for_car: PartsForCarCreateSchema) -> PartsForCarSchema:
    parts_for_car_repo = PartsForCarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_for_car_repo.check_connection(session=session)
        new_part_for_car = await parts_for_car_repo.add_part_for_car(part_for_car=part_for_car, session=session)

    return new_part_for_car


@router.delete("/delete_part_for_car/{part_for_car_id}", response_model=dict)
async def delete_part_for_car(part_for_car_id: int) -> dict:
    parts_for_car_repo = PartsForCarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await parts_for_car_repo.check_connection(session=session)
        deleted = await parts_for_car_repo.delete_part_for_car(part_for_car_id=part_for_car_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Part for car not found")

    return {"detail": "Part for car deleted successfully"}


@router.get("/all_receipts", response_model=list[ReceiptSchema])
async def get_all_receipts() -> list[ReceiptSchema]:
    receipt_repo = ReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await receipt_repo.check_connection(session=session)
        all_receipts = await receipt_repo.get_all_receipts(session=session)

    return all_receipts


@router.get("/receipt/{receipt_id}", response_model=ReceiptSchema)
async def get_receipt_by_id(receipt_id: int) -> ReceiptSchema:
    receipt_repo = ReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await receipt_repo.check_connection(session=session)
        receipt = await receipt_repo.get_receipt_by_id(receipt_id=receipt_id, session=session)

        if receipt is None:
            raise HTTPException(status_code=404, detail="Receipt not found")

    return receipt


@router.post("/add_receipt", response_model=ReceiptSchema)
async def add_receipt(receipt: ReceiptCreateSchema) -> ReceiptSchema:
    receipt_repo = ReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await receipt_repo.check_connection(session=session)
        new_receipt = await receipt_repo.add_receipt(receipt=receipt, session=session)

    return new_receipt


@router.delete("/delete_receipt/{receipt_id}", response_model=dict)
async def delete_receipt(receipt_id: int) -> dict:
    receipt_repo = ReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await receipt_repo.check_connection(session=session)
        deleted = await receipt_repo.delete_receipt(receipt_id=receipt_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Receipt not found")

    return {"detail": "Receipt deleted successfully"}


@router.get("/all_service_receipts", response_model=list[ServiceReceiptSchema])
async def get_all_service_receipts() -> list[ServiceReceiptSchema]:
    service_receipt_repo = ServiceReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_receipt_repo.check_connection(session=session)
        all_service_receipts = await service_receipt_repo.get_all_service_receipts(session=session)

    return all_service_receipts


@router.get("/service_receipt/{service_receipt_id}", response_model=ServiceReceiptSchema)
async def get_service_receipt_by_id(service_receipt_id: int) -> ServiceReceiptSchema:
    service_receipt_repo = ServiceReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_receipt_repo.check_connection(session=session)
        service_receipt = await service_receipt_repo.get_service_receipt_by_id(service_receipt_id=service_receipt_id, session=session)

        if service_receipt is None:
            raise HTTPException(status_code=404, detail="Service receipt not found")

    return service_receipt


@router.post("/add_service_receipt", response_model=ServiceReceiptSchema)
async def add_service_receipt(service_receipt: ServiceReceiptCreateSchema) -> ServiceReceiptSchema:
    service_receipt_repo = ServiceReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_receipt_repo.check_connection(session=session)
        new_service_receipt = await service_receipt_repo.add_service_receipt(service_receipt=service_receipt, session=session)

    return new_service_receipt


@router.delete("/delete_service_receipt/{service_receipt_id}", response_model=dict)
async def delete_service_receipt(service_receipt_id: int) -> dict:
    service_receipt_repo = ServiceReceiptRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await service_receipt_repo.check_connection(session=session)
        deleted = await service_receipt_repo.delete_service_receipt(service_receipt_id=service_receipt_id, session=session)

        if not deleted:
            raise HTTPException(status_code=404, detail="Service receipt not found")

    return {"detail": "Service receipt deleted successfully"}
