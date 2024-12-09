from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from products.crud import create_product, get_product, get_all_products, update_product, delete_product
from products.schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)


@router.get("/{product_id}", response_model=ProductResponse)
def retrieve_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/", response_model=list[ProductResponse])
def list_all_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}
