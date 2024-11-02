from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class ClientCreateSchema(BaseModel):
    full_name: str
    date_of_birth: date
    phone_number: str
    total_amount_of_work: int | None = Field(default=None)


class ClientsSchema(ClientCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
