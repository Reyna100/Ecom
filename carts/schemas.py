from pydantic import BaseModel
from typing import Optional, List

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class CartItemResponse(CartItemBase):
    id: int


class CartBase(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class CartResponse(CartBase):
    id: int
    total: float
    items: List[CartItemResponse] = []


class AddCartItem(CartItemBase):
    pass
