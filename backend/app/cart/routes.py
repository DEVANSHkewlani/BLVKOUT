from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from uuid import UUID

from app.core.database import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.cart.schemas import (

    AddToCartSchema,

    UpdateCartSchema,

    CartResponse
)

from app.cart.service import (

    fetch_cart,

    add_to_cart,

    update_cart_quantity,

    remove_cart_item
)


router = APIRouter()


@router.get(
    "/",
    response_model=list[CartResponse]
)
async def get_cart(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return fetch_cart(
        db,
        current_user
    )


@router.post(
    "/add",
    response_model=CartResponse
)
async def add_product_to_cart(

    cart_data: AddToCartSchema,

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return add_to_cart(
        db,
        current_user,
        cart_data
    )


@router.put(
    "/{cart_item_id}",
    response_model=CartResponse
)
async def update_cart_item_qty(

    cart_item_id: UUID,

    update_data: UpdateCartSchema,

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return update_cart_quantity(
        db,
        cart_item_id,
        update_data.qty
    )


@router.delete("/{cart_item_id}")
async def delete_cart_item_route(

    cart_item_id: UUID,

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    remove_cart_item(
        db,
        cart_item_id
    )

    return {
        "message": "Cart item removed"
    }