# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr

class TokenData(BaseModel):
    email: Optional[EmailStr]