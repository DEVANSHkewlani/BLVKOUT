from sqlalchemy.orm import Session

from app.cart.models import CartItem


def get_user_cart(
    db: Session,
    user_id
):

    return db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).all()


def get_cart_item(
    db: Session,
    user_id,
    product_id,
    size,
    color
):

    return db.query(CartItem).filter(

        CartItem.user_id == user_id,

        CartItem.product_id == product_id,

        CartItem.size == size,

        CartItem.color == color

    ).first()


def get_cart_item_by_id(
    db: Session,
    cart_item_id
):

    return db.query(CartItem).filter(
        CartItem.id == cart_item_id
    ).first()


def create_cart_item(
    db: Session,
    cart_item
):

    db.add(cart_item)

    db.commit()

    db.refresh(cart_item)

    return cart_item


def update_cart_item(
    db: Session,
    cart_item
):

    db.commit()

    db.refresh(cart_item)

    return cart_item


def delete_cart_item(
    db: Session,
    cart_item
):

    db.delete(cart_item)

    db.commit()