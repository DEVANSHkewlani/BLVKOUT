from slugify import slugify
from app.collections.models import Collection
from app.collections.repository import (
    get_all_collections,
    get_active_collections,
    get_collection_by_id,
    get_collection_by_slug,
    create_collection,
    update_collection,
    delete_collection
)
from app.collections.schemas import (
    CollectionCreate,
    CollectionUpdate
)


def fetch_all_collections(db):
    return get_all_collections(db)


def fetch_active_collections(db):
    return get_active_collections(db)


def fetch_collection(db, collection_id):
    return get_collection_by_id(db, collection_id)


def create_new_collection(db, data: CollectionCreate):
    slug = slugify(data.name)
    existing = get_collection_by_slug(db, slug)
    if existing:
        raise ValueError("Collection already exists")

    new_collection = Collection(
        name=data.name,
        slug=slug,
        description=data.description,
        image_url=data.image_url,
        is_active=data.is_active
    )
    return create_collection(db, new_collection)


def edit_collection(db, collection, data: CollectionUpdate):
    for key, value in data.model_dump(
        exclude_unset=True
    ).items():
        if key == "name" and value:
            setattr(collection, "slug", slugify(value))
        setattr(collection, key, value)
    return update_collection(db, collection)


def remove_collection(db, collection):
    delete_collection(db, collection)
