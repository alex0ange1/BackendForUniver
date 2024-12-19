from pydantic import BaseModel, ConfigDict
from datetime import date

class ReceiptCreateSchema(BaseModel):
    client_id: int
    service_receipt_id: int
    car_id: int
    date: date
    cost: int

class ReceiptSchema(ReceiptCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
