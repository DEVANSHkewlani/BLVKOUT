from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

from app.core.database import get_db
from app.auth.roles import get_current_admin
from app.user.models import User
from app.orders.models import Order


router = APIRouter()


class CustomerResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: Optional[datetime] = None
    order_count: int = 0
    total_spent: Decimal = Decimal("0.00")

    class Config:
        from_attributes = True


class CustomerStatusUpdate(BaseModel):
    is_active: bool


@router.get("/")
async def get_all_customers(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin only: list all users with order stats"""
    users = db.query(User).order_by(
        desc(User.created_at)
    ).all()

    results = []
    for user in users:
        order_stats = db.query(
            func.count(Order.id).label("count"),
            func.coalesce(
                func.sum(Order.total), 0
            ).label("total")
        ).filter(
            Order.user_id == user.id
        ).first()

        results.append({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
            "phone": user.phone,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "order_count": order_stats.count if order_stats else 0,
            "total_spent": float(order_stats.total) if order_stats else 0
        })

    return results


@router.put("/{user_id}")
async def update_customer_status(
    user_id: UUID,
    data: CustomerStatusUpdate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin only: block/unblock a customer"""
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    return {
        "message": f"Customer {'activated' if data.is_active else 'blocked'} successfully",
        "id": str(user.id),
        "is_active": user.is_active
    }
