from pydantic import BaseModel, ConfigDict

class CarsStatusCreateSchema(BaseModel):
    car_sts: str
    owner_id: int
    cost_of_provided_services: int

class CarsStatusSchema(CarsStatusCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
