from fastapi import HTTPException

from app.wishlist.models import (
    WishlistItem
)

from app.wishlist.repository import (

    get_user_wishlist,

    get_wishlist_item,

    create_wishlist_item,

    delete_wishlist_item
)

from app.products.repository import (
    get_product_by_id
)

from app.user.repository import (
    get_user_by_auth_id
)


def fetch_user_wishlist(
    db,
    current_user
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    return get_user_wishlist(
        db,
        user.id
    )


def add_to_wishlist(
    db,
    current_user,
    product_id
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    product = get_product_by_id(
        db,
        product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_item = get_wishlist_item(
        db,
        user.id,
        product_id
    )

    if existing_item:

        raise HTTPException(
            status_code=400,
            detail="Product already in wishlist"
        )

    wishlist_item = WishlistItem(
        user_id=user.id,
        product_id=product_id
    )

    return create_wishlist_item(
        db,
        wishlist_item
    )


def remove_from_wishlist(
    db,
    current_user,
    product_id
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    wishlist_item = get_wishlist_item(
        db,
        user.id,
        product_id
    )

    if not wishlist_item:

        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found"
        )

    delete_wishlist_item(
        db,
        wishlist_item
    )