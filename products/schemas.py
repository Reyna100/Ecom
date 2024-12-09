from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class ProductResponse(ProductBase):
    id: int
