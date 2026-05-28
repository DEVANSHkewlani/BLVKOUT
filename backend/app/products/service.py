from app.products.repository import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
    get_product_by_slug
)
from slugify import slugify
from app.products.models import Product

from app.products.schemas import (
    ProductCreate,
    ProductUpdate
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

def create_new_product(
    db,
    product_data: ProductCreate
):

    slug = slugify(product_data.name)

    existing_product = get_product_by_slug(
        db,
        slug
    )

    if existing_product:
        raise ValueError(
            "Product already exists"
        )

    new_product = Product(
        **product_data.model_dump(),
        slug=slug,
        status="active"
    )

    return create_product(
        db,
        new_product
    )

def edit_product(
    db,
    product,
    update_data: ProductUpdate
):

    for key, value in update_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(product, key, value)

    return update_product(
        db,
        product
    )

def remove_product(
    db,
    product
):

    delete_product(
        db,
        product
    )