# Python
from typing import Optional
from datetime import date

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

class UserBase(BaseModel):
    email: EmailStr = Field(...)

    class Config():
        orm_mode = True


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    birthday: Optional[date] = Field(default=None)


class UserRegister(User, UserLogin):
    pass

 