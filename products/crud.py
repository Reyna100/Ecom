from sqlalchemy.orm import Session
from products.models import Product
from products.schemas import ProductCreate, ProductUpdate

def create_product(db: Session, product: ProductCreate):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_all_products(db: Session):
    return db.query(Product).all()


def update_product(db: Session, product_id: int, product: ProductUpdate):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        return None
    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)
    db.commit()
    db.refresh(existing_product)
    return existing_product


def delete_product(db: Session, product_id: int):
    product_to_delete = db.query(Product).filter(Product.id == product_id).first()
    if not product_to_delete:
        return None
    db.delete(product_to_delete)
    db.commit()
    return product_to_delete
