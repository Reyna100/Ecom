from sqlalchemy.orm import Session
from carts.models import Cart, CartItem
from carts.schemas import AddCartItem

def get_user_cart(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()


def add_item_to_cart(db: Session, user_id: int, item: AddCartItem):
    cart = get_user_cart(db, user_id)
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id)
        .first()
    )
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    update_cart_total(db, cart.id)
    return cart


def remove_item_from_cart(db: Session, user_id: int, item_id: int):
    cart = get_user_cart(db, user_id)
    if not cart:
        return None

    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.id == item_id).first()
    if not cart_item:
        return None

    db.delete(cart_item)
    db.commit()
    update_cart_total(db, cart.id)
    return cart


def update_cart_total(db: Session, cart_id: int):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        return

    total = 0
    for item in cart.items:
        total += item.quantity * get_product_price(db, item.product_id)

    cart.total = total
    db.commit()


def get_product_price(db: Session, product_id: int):
    from products.models import Product

    product = db.query(Product).filter(Product.id == product_id).first()
    return product.price if product else 0.0


def view_cart(db: Session, user_id: int):
    return get_user_cart(db, user_id)
