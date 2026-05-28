from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import ARRAY

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
    price = Column(
    Numeric(10, 2),
    nullable=False
    )

    sale_price = Column(
    Numeric(10, 2),
    nullable=True
)

    status = Column(
    String,
    default="active"
)

    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False
    )

    images = Column(
    ARRAY(String),
    default=[]
)

    sizes = Column(
    ARRAY(String),
    default=[]
)

    colors = Column(
    ARRAY(String),
    default=[]
)

    fabric = Column(
    String,
    nullable=True
)

    tags = Column(
    ARRAY(String),
    default=[]
)   
    updated_at = Column(
    TIMESTAMP(timezone=True),
    server_default=func.now(),
    onupdate=func.now()
)