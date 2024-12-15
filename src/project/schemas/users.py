from datetime import date

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserCreateUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: str = Field(pattern=r"^\S+@\S+\.\S+$", examples=["email@mail.ru"])
    password: str
    phone_number: str | None = Field(default=None, pattern=r"^\+?7\d{10}$", examples=["+79999999999"])
    is_admin: bool = False


class UserSchema(UserCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int