from sqlalchemy.orm import Session
from orders.models import Order, OrderItem
from products.models import Product
from carts.models import Cart, CartItem
from orders.schemas import OrderCreate
from typing import List

def create_order(db: Session, user_id: int, items: OrderCreate, total_amount: float):
    order = Order(user_id=user_id, total_amount=total_amount)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price * item.quantity,
        )
        db.add(order_item)
    db.commit()
    return order


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        return order
    return None


def calculate_total_amount(items: OrderCreate, db: Session):
    total_amount = 0
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            total_amount += item.quantity * product.price
    return total_amount
