from fastapi import FastAPI
from database import engine, Base
from users.routes import router as users_router
from products.routes import router as products_router
from carts.routes import router as carts_router
from orders.routes import router as orders_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(carts_router, prefix="/carts", tags=["Carts"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
