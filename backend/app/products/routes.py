from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from uuid import UUID
from app.products.models import Product
from fastapi import HTTPException

router = APIRouter()



@router.get("/")
async def get_products(
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return {
        "count": len(products)
    }
@router.get("/{product_id}")
async def get_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product