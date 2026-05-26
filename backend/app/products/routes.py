from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from uuid import UUID
from typing import List

from app.core.database import get_db

from app.products.schemas import ProductResponse

from app.products.service import (
    fetch_products,
    fetch_product
)


router = APIRouter()


@router.get(
    "/",
    response_model=List[ProductResponse]
)
async def get_products(
    db: Session = Depends(get_db)
):

    return fetch_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):

    product = fetch_product(
        db,
        product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product