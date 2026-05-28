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

from fastapi.middleware.cors import CORSMiddleware

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