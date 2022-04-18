from pydantic import BaseModel


from datetime import datetime
from vitemaprog.requests.right_request import Right

class Role(BaseModel):
    uuid: str
    label: str
    slug: str
    rights: list
    created_at: datetime
    updated_at: datetime

class RoleCreate(BaseModel):
    label: str
    is_admin: bool = False
    slug: str
