from sqlalchemy.orm import Session
from app.collections.models import Collection


def get_all_collections(db: Session):
    return db.query(Collection).all()


def get_active_collections(db: Session):
    return db.query(Collection).filter(
        Collection.is_active == True
    ).all()


def get_collection_by_id(db: Session, collection_id):
    return db.query(Collection).filter(
        Collection.id == collection_id
    ).first()


def get_collection_by_slug(db: Session, slug: str):
    return db.query(Collection).filter(
        Collection.slug == slug
    ).first()


def create_collection(db: Session, collection: Collection):
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


def update_collection(db: Session, collection: Collection):
    db.commit()
    db.refresh(collection)
    return collection


def delete_collection(db: Session, collection: Collection):
    db.delete(collection)
    db.commit()
