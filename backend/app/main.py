from fastapi import FastAPI
from app.products.routes import router as products_router

app = FastAPI(
    title="BLVKOUT API",
    version="1.0.0"
)

app.include_router(
    products_router,
    prefix="/products",
    tags=["Products"]
)


@app.get("/")
async def root():
    return {
        "message": "BLVKOUT Backend Running"
    }