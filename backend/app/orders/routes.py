from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.auth.roles import get_current_admin
from app.auth.dependencies import get_current_user
from app.orders.models import Order
from app.orders.schemas import (
    OrderResponse,
    OrderStatusUpdate
)


router = APIRouter()


@router.get(
    "/",
    response_model=List[OrderResponse]
)
async def get_all_orders(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin only: list all orders"""
    return db.query(Order).order_by(
        desc(Order.created_at)
    ).all()


@router.get(
    "/me",
    response_model=List[OrderResponse]
)
async def get_my_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Customer: list my own orders"""
    return db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(
        desc(Order.created_at)
    ).all()


@router.put(
    "/{order_id}",
    response_model=OrderResponse
)
async def update_order_status(
    order_id: UUID,
    data: OrderStatusUpdate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin only: update order status"""
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = data.status
    db.commit()
    db.refresh(order)
    return order
