from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from vitemaprog.db import Base
import uuid
from vitemaprog.requests import UserOut

__all__ = ["User"]

class User(Base):
    __tablename__ = 'users'

    __model_out__ = UserOut

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

