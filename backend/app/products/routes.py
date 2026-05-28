from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.products.schemas import (
    ProductCreate,
    ProductUpdate
)
from sqlalchemy.orm import Session

from uuid import UUID
from typing import List

from app.core.database import get_db

from app.products.schemas import ProductResponse

from app.products.service import (
    fetch_products,
    fetch_product,
    create_new_product,
    edit_product,
    remove_product
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

@router.post(
    "/",
    response_model=ProductResponse
)
async def create_product_route(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):

    return create_new_product(
        db,
        product_data
    )

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
async def update_product_route(
    product_id: UUID,
    update_data: ProductUpdate,
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

    return edit_product(
        db,
        product,
        update_data
    )

@router.delete("/{product_id}")
async def delete_product_route(
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

    remove_product(
        db,
        product
    )

    return {
        "message": "Product deleted successfully"
    }