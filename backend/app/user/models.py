from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True
    )

    email = Column(
        String,
        nullable=False,
        unique=True
    )

    full_name = Column(
        String,
        nullable=True
    )

    avatar_url = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    role = Column(
        String,
        default="customer"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )