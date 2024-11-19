from pydantic import BaseModel, ConfigDict

class PartsForCarCreateSchema(BaseModel):
    part_id: int
    car_id: int

class PartsForCarSchema(PartsForCarCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
