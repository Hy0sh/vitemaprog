from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

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
    created_at: datetime
    updated_at: datetime
