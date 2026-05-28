from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid

from app.core.database import Base


class SiteContent(Base):
    __tablename__ = "site_content"

    key = Column(
        String,
        primary_key=True,
        nullable=False
    )

    value = Column(
        Text,
        nullable=False,
        default=""
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
