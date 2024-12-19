import datetime
from pydantic import BaseModel, ConfigDict


# Pydantic schema for receipt details
class ReceiptDetailsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    receipt_date: datetime.date
    total_cost: int
    client_name: str
    car_model: str
    car_sts: str
    service_name: str
    service_cost: int
    part_name: str
    part_selling_price: int