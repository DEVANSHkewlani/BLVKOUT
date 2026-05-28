from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta

from app.core.database import get_db
from app.auth.roles import get_current_admin
from app.user.models import User
from app.orders.models import Order
from app.products.models import Product


router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin only: dashboard KPI stats"""
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Total revenue
    total_revenue = db.query(
        func.coalesce(func.sum(Order.total), 0)
    ).scalar()

    # Orders today
    orders_today = db.query(
        func.count(Order.id)
    ).filter(
        cast(Order.created_at, Date) == today
    ).scalar()

    # Total orders
    total_orders = db.query(
        func.count(Order.id)
    ).scalar()

    # Avg order value
    avg_order = db.query(
        func.coalesce(func.avg(Order.total), 0)
    ).scalar()

    # Active products
    active_products = db.query(
        func.count(Product.id)
    ).filter(
        Product.status == "active"
    ).scalar()

    # Total customers
    total_customers = db.query(
        func.count(User.id)
    ).filter(
        User.role == "customer"
    ).scalar()

    # New customers (last 7 days)
    new_customers = db.query(
        func.count(User.id)
    ).filter(
        User.role == "customer",
        cast(User.created_at, Date) >= week_ago
    ).scalar()

    # Order status counts
    pending = db.query(func.count(Order.id)).filter(Order.status == "pending").scalar()
    processing = db.query(func.count(Order.id)).filter(Order.status == "processing").scalar()
    shipped = db.query(func.count(Order.id)).filter(Order.status == "shipped").scalar()
    delivered = db.query(func.count(Order.id)).filter(Order.status == "delivered").scalar()

    return {
        "total_revenue": float(total_revenue),
        "orders_today": orders_today,
        "total_orders": total_orders,
        "avg_order_value": round(float(avg_order), 2),
        "active_products": active_products,
        "total_customers": total_customers,
        "new_customers": new_customers,
        "order_statuses": {
            "pending": pending,
            "processing": processing,
            "shipped": shipped,
            "delivered": delivered
        }
    }
