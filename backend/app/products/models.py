from sqlalchemy import Column, String, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    slug = Column(String, unique=True, nullable=False)

    description = Column(Text)

    stock_qty = Column(Integer, default=0)

    is_featured = Column(Boolean, default=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )