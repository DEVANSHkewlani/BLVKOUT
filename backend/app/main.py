from fastapi import FastAPI
from app.products.routes import router as products_router
from app.auth.routes import router as auth_router
from app.user.routes import (
    router as profile_router
)
from app.wishlist.routes import (
    router as wishlist_router
)
from app.cart.routes import (
    router as cart_router
)
from app.policies.routes import (
    router as policies_router
)
from app.support.routes import (
    router as support_router
)
from app.content.routes import (
    router as content_router
)
from app.collections.routes import (
    router as collections_router
)
from app.orders.routes import (
    router as orders_router
)
from app.customers.routes import (
    router as customers_router
)
from app.admin.routes import (
    router as admin_router
)

from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.content.models import SiteContent
from app.collections.models import Collection

# Create all tables in database one by one if they do not exist
for table_name, table in Base.metadata.tables.items():
    try:
        # checkfirst=True avoids creating if it already exists
        table.create(bind=engine, checkfirst=True)
        print(f"Database table '{table_name}' initialized successfully.")
    except Exception as e:
        print(f"Database table '{table_name}' initialization warning: {e}")

app = FastAPI(
    title="BLVKOUT API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "BLVKOUT Backend Running"
    }

app.include_router(
    products_router,
    prefix="/products",
    tags=["Products"]
)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
app.include_router(
    profile_router,
    prefix="/profile",
    tags=["Profile"]
)
app.include_router(
    wishlist_router,
    prefix="/wishlist",
    tags=["Wishlist"]
)
app.include_router(
    cart_router,
    prefix="/cart",
    tags=["Cart"]
)
app.include_router(
    policies_router,
    prefix="/policies",
    tags=["Policies"]
)
app.include_router(
    support_router,
    prefix="/support",
    tags=["Support"]
)
app.include_router(
    content_router,
    prefix="/content",
    tags=["Content"]
)
app.include_router(
    collections_router,
    prefix="/collections",
    tags=["Collections"]
)
app.include_router(
    orders_router,
    prefix="/orders",
    tags=["Orders"]
)
app.include_router(
    customers_router,
    prefix="/customers",
    tags=["Customers"]
)
app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)