from sqlalchemy.orm import Session

from app.wishlist.models import (
    WishlistItem
)


def get_user_wishlist(
    db: Session,
    user_id
):

    return db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id
    ).all()


def get_wishlist_item(
    db: Session,
    user_id,
    product_id
):

    return db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id,
        WishlistItem.product_id == product_id
    ).first()


def create_wishlist_item(
    db: Session,
    wishlist_item
):

    db.add(wishlist_item)

    db.commit()

    db.refresh(wishlist_item)

    return wishlist_item


def delete_wishlist_item(
    db: Session,
    wishlist_item
):

    db.delete(wishlist_item)

    db.commit()