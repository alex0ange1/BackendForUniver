from pydantic import BaseModel, ConfigDict

class ServiceCreateSchema(BaseModel):
    name: str
    service_cost: int
    part_id: int | None

class ServiceSchema(ServiceCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int