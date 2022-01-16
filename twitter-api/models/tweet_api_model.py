# Python
from typing import Optional
from datetime import date

# Path 
from .user_api_model import User

# Pydantic
from pydantic import BaseModel
from pydantic import Field

class Tweet(BaseModel):
    
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: date = Field(default=date.today())
    updated_at: Optional[date] = Field(default=None)
    # author
    #by: User = Field(...)

    class Config():
        orm_mode = True
    