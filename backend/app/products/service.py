from app.products.repository import (
    get_all_products,
    get_product_by_id
)


def fetch_products(db):

    return get_all_products(db)


def fetch_product(
    db,
    product_id
):

    return get_product_by_id(
        db,
        product_id
    )