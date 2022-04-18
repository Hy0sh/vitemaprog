from pydantic import BaseModel


from datetime import datetime

class Role(BaseModel):
    uuid: str
    label: str
    slug: str
    created_at: datetime
    updated_at: datetime

class RoleCreate(BaseModel):
    label: str
    is_admin: bool = False
