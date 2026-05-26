from sqlalchemy.orm import Session

from app.products.models import Product


def get_all_products(db: Session):

    return db.query(Product).all()


def get_product_by_id(
    db: Session,
    product_id
):

    return db.query(Product).filter(
        Product.id == product_id
    ).first()