
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from vitemaprog.database import BaseModel
import uuid
from vitemaprog.requests.role_request import Role


role_right = Table('roles_rights', BaseModel.metadata,
    Column('role_uuid', UUID(as_uuid=True), ForeignKey('roles.uuid', ondelete='CASCADE'), primary_key=True),
    Column('right_uuid', UUID(as_uuid=True), ForeignKey('rights.uuid', ondelete='CASCADE'), primary_key=True)
)

__all__ = ["RoleModel"]
class RoleModel(BaseModel):
    __tablename__ = 'roles'

    __model_out__ = Role

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    rights_bdd = relationship('RightModel', secondary=role_right)

    @property
    def rights(self) -> list:
        return [right.slug for right in self.rights_bdd]

    def __repr__(self) -> str:
        return f"<RoleModel: {self.label}[{self.slug}]>"
