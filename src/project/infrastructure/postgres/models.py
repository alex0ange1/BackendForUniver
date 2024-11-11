from datetime import date

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from project.infrastructure.postgres.database import Base


class Clients(Base):
    __tablename__ = "clients_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    total_amount_of_work: Mapped[int] = mapped_column(nullable=True)


class Cars(Base):
    __tablename__ = "cars_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    make_and_model: Mapped[str] = mapped_column(nullable=False)
    sts: Mapped[str] = mapped_column(nullable=False, unique=True)
    year_of_issue: Mapped[int] = mapped_column(nullable=False)
    engine_displacement: Mapped[float] = mapped_column(nullable=False)


class Workers(Base):
    __tablename__ = "workers_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    experience: Mapped[int] = mapped_column(nullable=False)
    salary: Mapped[int] = mapped_column(nullable=False)


class Parts(Base):
    __tablename__ = "parts_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country_of_manufacture: Mapped[str] = mapped_column(nullable=False)
    purchase_price: Mapped[int] = mapped_column(nullable=False)
    selling_price: Mapped[int] = mapped_column(nullable=False, unique=True)
    status: Mapped[str] = mapped_column(nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(nullable=False)


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    service_cost: Mapped[int] = mapped_column(nullable=False, unique=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts_list.id"), nullable=True)


class CarsStatus(Base):
    __tablename__ = "cars_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    car_sts: Mapped[str] = mapped_column(ForeignKey("cars_list.sts"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("clients_list.id"), nullable=False)
    cost_of_provided_services: Mapped[int] = mapped_column(nullable=False)
    __table_args__ = (
        UniqueConstraint('car_sts', name='uq_car_sts'),
        UniqueConstraint('owner_id', name='uq_owner_id'),
    )


class WorkersAbleToProvideService(Base):
    __tablename__ = "workers_able_to_provide_service"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers_list.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), nullable=False)


class PartsForCar(Base):
    __tablename__ = "parts_for_car"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts_list.id"), nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars_list.id"), nullable=False)


class Receipt(Base):
    __tablename__ = "receipt"

    service_receipt_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients_list.id"), nullable=False)
    car_sts: Mapped[str] = mapped_column(ForeignKey("cars_list.sts"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)


class ServiceReceipt(Base):
    __tablename__ = "service_receipt"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), nullable=False)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts_list.id"), nullable=False)
    quantity_of_parts: Mapped[int] = mapped_column(nullable=False)
    part_cost: Mapped[int] = mapped_column(ForeignKey("parts_list.selling_price"), nullable=False)
    selling_cost: Mapped[int] = mapped_column(ForeignKey("service.service_cost"), nullable=False)