from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from carts.crud import add_item_to_cart, remove_item_from_cart, view_cart
from carts.schemas import AddCartItem, CartResponse

router = APIRouter()


@router.get("/", response_model=CartResponse)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = view_cart(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/", response_model=CartResponse)
def add_cart_item(user_id: int, item: AddCartItem, db: Session = Depends(get_db)):
    return add_item_to_cart(db, user_id, item)


@router.delete("/{item_id}", response_model=CartResponse)
def remove_cart_item(user_id: int, item_id: int, db: Session = Depends(get_db)):
    cart = remove_item_from_cart(db, user_id, item_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart or item not found")
    return cart
