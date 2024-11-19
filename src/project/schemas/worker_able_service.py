from pydantic import BaseModel, ConfigDict

class WorkersAbleToProvideServiceCreateSchema(BaseModel):
    worker_id: int
    service_id: int

class WorkersAbleToProvideServiceSchema(WorkersAbleToProvideServiceCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
