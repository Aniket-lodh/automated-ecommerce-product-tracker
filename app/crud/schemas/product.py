from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Products pydantic model and sqlAlchemy model
class ProductsBase(BaseModel):
    name: str
    url: str
    price: float
    availability: bool
    last_checked: Optional[datetime] = None


class ProductCreate(ProductsBase):
    pass


class Products(ProductsBase):
    id: int

    class Config:
        from_attributes: True


# Tracked Products pydantic model and sqlAlchemy model
class TrackedProductsBase(BaseModel):
    user_id: int
    product_id: int
    target_price: float
    notified: bool


class TrackedProductsCreate(TrackedProductsBase):
    pass


class TrackedProduct(TrackedProductsBase):
    id: int

    class Config:
        from_attributes: True
