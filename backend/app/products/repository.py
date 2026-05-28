from sqlalchemy.orm import Session
from app.products.schemas import ProductCreate
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

def create_product(
    db: Session,
    product_data
):

    db.add(product_data)

    db.commit()

    db.refresh(product_data)

    return product_data

def update_product(
    db: Session,
    product
):

    db.commit()

    db.refresh(product)

    return product

def delete_product(
    db: Session,
    product
):

    db.delete(product)

    db.commit()

def get_product_by_slug(
    db: Session,
    slug: str
):

    return db.query(Product).filter(
        Product.slug == slug
    ).first()