from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from vitemaprog.models.auth.role_model import RoleModel
from vitemaprog.requests.role_request import Role



class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role_uuid: str
    @validator('role_uuid', always=True)
    def check_role_uuid(value) -> str:
        if not RoleModel.exists(value):
            raise ValueError('Role does not exist')
        return str(value)


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    role_uuid: Optional[str]
    @validator('role_uuid', always=True)
    def check_role_uuid(value) -> str:
        if value is not None and not RoleModel.exists(value):
            raise ValueError('Role does not exist')
        return value

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('passwords do not match')
        return v

class User(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: str
    role: Role
    created_at: datetime
    updated_at: datetime



