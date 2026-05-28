from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import List, Optional

class ProductBase(BaseModel):

    name: str

    description: Optional[str] = None

    price: Decimal

    sale_price: Optional[Decimal] = None

    stock_qty: int

    category_id: UUID

    images: List[str] = []

    sizes: List[str] = []

    colors: List[str] = []

    fabric: Optional[str] = None

    tags: List[str] = []

    is_featured: bool = False

class ProductResponse(ProductBase):

    id: UUID

    slug: str

    status: str

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    price: Optional[Decimal] = None

    sale_price: Optional[Decimal] = None

    stock_qty: Optional[int] = None

    category_id: Optional[UUID] = None

    images: Optional[List[str]] = None

    sizes: Optional[List[str]] = None

    colors: Optional[List[str]] = None

    fabric: Optional[str] = None

    tags: Optional[List[str]] = None

    is_featured: Optional[bool] = None

    status: Optional[str] = None