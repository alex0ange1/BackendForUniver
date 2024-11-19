from pydantic import BaseModel, Field, ConfigDict


class CarsCreateSchema(BaseModel):
    make_and_model: str
    sts: str
    year_of_issue: int
    engine_displacement: float


class CarsSchema(CarsCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int