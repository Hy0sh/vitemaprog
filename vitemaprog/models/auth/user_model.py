from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime,ForeignKey
from vitemaprog.database import BaseModel
from sqlalchemy.orm import relationship
import uuid
from vitemaprog.requests import User
import crypt
from hmac import compare_digest

__all__ = ["UserModel"]
class UserModel(BaseModel):
    __tablename__ = 'users'

    __model_out__ = User

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_uuid = Column(UUID(as_uuid=True), ForeignKey('roles.uuid', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    role = relationship('RoleModel')

    def hash_password(password) -> str:
        return crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))

    def validate_password(self,password_plaintext) -> bool:
        return compare_digest(self.password, crypt.crypt(password_plaintext, self.password))

    def __repr__(self) -> str:
        return f"<UserModel: {self.first_name} {self.last_name}[{self.email}]>"

