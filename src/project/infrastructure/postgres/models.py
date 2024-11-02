from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from project.infrastructure.postgres.database import Base


class Clients(Base):
	__tablename__ = "clients_list"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	full_name: Mapped[str] = mapped_column(nullable=False)
	date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
	phone_number: Mapped[str] = mapped_column(nullable=False)
	total_amount_of_work: Mapped[int] = mapped_column(nullable=True)



