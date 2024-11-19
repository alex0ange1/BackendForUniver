from pydantic import BaseModel, ConfigDict

class WorkersCreateSchema(BaseModel):
    full_name: str
    experience: int
    salary: int

class WorkersSchema(WorkersCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int