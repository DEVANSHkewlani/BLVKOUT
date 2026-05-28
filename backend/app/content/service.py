from app.content.repository import (
    get_all_content,
    upsert_content
)


def fetch_all_content(db):
    return get_all_content(db)


def bulk_upsert_content(db, items: dict):
    results = []
    for key, value in items.items():
        result = upsert_content(db, key, value)
        results.append(result)
    return results
