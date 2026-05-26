from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import List, Optional


class ProductResponse(BaseModel):

    id: UUID

    name: str

    slug: str

    description: Optional[str]

    price: Decimal

    sale_price: Optional[Decimal]

    stock_qty: int

    status: str

    images: List[str]

    sizes: List[str]

    colors: List[str]

    fabric: Optional[str]

    tags: List[str]

    is_featured: bool

    class Config:
        from_attributes = True