from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class ClientsSchema(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	full_name: str
	date_of_birth: date
	phone_number: str
	total_amount_of_work: int | None = Field(default=None)


class ClientCreateSchema(BaseModel):
    full_name: str
    date_of_birth: date
    phone_number: str
    total_amount_of_work: int | None = Field(default=None)