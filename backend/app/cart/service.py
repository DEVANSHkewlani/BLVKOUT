from fastapi import HTTPException

from app.cart.models import CartItem

from app.cart.repository import (

    get_user_cart,

    get_cart_item,

    get_cart_item_by_id,

    create_cart_item,

    update_cart_item,

    delete_cart_item
)

from app.products.repository import (
    get_product_by_id
)

from app.user.repository import (
    get_user_by_auth_id
)


def fetch_cart(
    db,
    current_user
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    return get_user_cart(
        db,
        user.id
    )


def add_to_cart(
    db,
    current_user,
    cart_data
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    product = get_product_by_id(
        db,
        cart_data.product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_item = get_cart_item(
        db,
        user.id,
        cart_data.product_id,
        cart_data.size,
        cart_data.color
    )

    if existing_item:

        existing_item.qty += cart_data.qty

        return update_cart_item(
            db,
            existing_item
        )

    cart_item = CartItem(

        user_id=user.id,

        product_id=cart_data.product_id,

        qty=cart_data.qty,

        size=cart_data.size,

        color=cart_data.color
    )

    return create_cart_item(
        db,
        cart_item
    )


def update_cart_quantity(
    db,
    cart_item_id,
    qty
):

    cart_item = get_cart_item_by_id(
        db,
        cart_item_id
    )

    if not cart_item:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.qty = qty

    return update_cart_item(
        db,
        cart_item
    )


def remove_cart_item(
    db,
    cart_item_id
):

    cart_item = get_cart_item_by_id(
        db,
        cart_item_id
    )

    if not cart_item:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    delete_cart_item(
        db,
        cart_item
    )