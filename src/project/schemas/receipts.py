from pydantic import BaseModel, ConfigDict
from datetime import date

class ReceiptCreateSchema(BaseModel):
    client_id: int
    car_sts: str
    date: date
    cost: int

class ReceiptSchema(ReceiptCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    service_receipt_id: int
