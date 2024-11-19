from pydantic import BaseModel, ConfigDict

class PartsCreateSchema(BaseModel):
    name: str
    country_of_manufacture: str
    purchase_price: int
    selling_price: int
    status: str
    quantity_in_stock: int

class PartsSchema(PartsCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int