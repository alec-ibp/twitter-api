# Python
from uuid import UUID
from typing import Optional
from datetime import datetime

# Path 
from .user_api_model import User

# Pydantic
from pydantic import BaseModel
from pydantic import Field

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    # author
    by: User = Field(...)
    