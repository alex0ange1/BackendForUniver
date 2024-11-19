from pydantic import BaseModel, ConfigDict

class ServiceReceiptCreateSchema(BaseModel):
    service_id: int
    part_id: int
    quantity_of_parts: int
    part_cost: int
    selling_cost: int

class ServiceReceiptSchema(ServiceReceiptCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int