import enum
import uuid
from core.database import Base, current_time

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Column,String,Boolean,DateTime, Enum


class Role(enum.Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=current_time)
    last_login = Column(DateTime, nullable=True)
    
    role = Column(Enum(Role), default=Role.USER, nullable=False)