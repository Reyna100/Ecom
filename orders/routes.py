from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from orders.schemas import OrderCreate, OrderResponse
from orders.crud import (
    create_order,
    get_order_by_id,
    get_user_orders,
    update_order_status,
    calculate_total_amount,
)
from database import get_db

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def place_order(user_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    total_amount = calculate_total_amount(order.items,db)

    new_order = create_order(db, user_id, order.items, total_amount)
    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/user/{user_id}", response_model=List[OrderResponse])
def get_orders(user_id: int, db: Session = Depends(get_db)):
    orders = get_user_orders(db, user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_status(order_id: int, status: str, db: Session = Depends(get_db)):
    updated_order = update_order_status(db, order_id, status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order
