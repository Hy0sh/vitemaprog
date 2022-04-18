from typing import Optional
from pydantic import BaseModel


from datetime import datetime

class Right(BaseModel):
    uuid: str
    label: str
    slug: str
    created_at: datetime
    updated_at: datetime

class RightCreate(BaseModel):
    label: str
    slug: str
    description: Optional[str] = None
