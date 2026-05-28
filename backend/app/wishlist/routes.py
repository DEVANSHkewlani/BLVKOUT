from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from uuid import UUID

from app.core.database import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.wishlist.schemas import (
    WishlistResponse
)

from app.wishlist.service import (

    fetch_user_wishlist,

    add_to_wishlist,

    remove_from_wishlist
)


router = APIRouter()


@router.get(
    "/",
    response_model=list[WishlistResponse]
)
async def get_wishlist(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return fetch_user_wishlist(
        db,
        current_user
    )


@router.post(
    "/{product_id}",
    response_model=WishlistResponse
)
async def add_product_to_wishlist(

    product_id: UUID,

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return add_to_wishlist(
        db,
        current_user,
        product_id
    )


@router.delete("/{product_id}")
async def delete_wishlist_item_route(

    product_id: UUID,

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    remove_from_wishlist(
        db,
        current_user,
        product_id
    )

    return {
        "message": "Removed from wishlist"
    }