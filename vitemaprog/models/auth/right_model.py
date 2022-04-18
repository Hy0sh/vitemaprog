
from vitemaprog.database import BaseModel
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from vitemaprog.requests import Right
import uuid

__all__ = ["RightModel"]
class RightModel(BaseModel):
    __tablename__ = 'rights'

    __model_out__ = Right

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False)
    description = Column(String, nullable=True)
    slug = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<RightModel: {self.label}[{self.slug}]>"
