from sqlalchemy.orm import Session
from app.content.models import SiteContent


def get_all_content(db: Session):
    return db.query(SiteContent).all()


def get_content_by_key(db: Session, key: str):
    return db.query(SiteContent).filter(
        SiteContent.key == key
    ).first()


def upsert_content(db: Session, key: str, value: str):
    existing = get_content_by_key(db, key)
    if existing:
        existing.value = value
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_item = SiteContent(key=key, value=value)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
