from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, Numeric
import uuid

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        String,
        default="pending"
    )

    total = Column(
        Numeric(10, 2),
        nullable=False
    )

    items = Column(
        JSONB,
        default=[]
    )

    shipping_address = Column(
        Text,
        nullable=True
    )

    customer_name = Column(
        String,
        nullable=True
    )

    customer_email = Column(
        String,
        nullable=True
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
