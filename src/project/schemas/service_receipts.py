from pydantic import BaseModel, ConfigDict

class ServiceReceiptCreateSchema(BaseModel):
    service_id: int
    part_id: int

class ServiceReceiptSchema(ServiceReceiptCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int