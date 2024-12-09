from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(OrderItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    total_amount: float


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        orm_mode = True
