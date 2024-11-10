from pydantic import BaseModel


class UsersBase(BaseModel):
    email: str


class Users(UsersBase):
    id: int

    class Config:
        from_attributes = True


class ProductsBase(BaseModel):
    name: str
    url: str
    price: float
    availability: bool
    last_checked: str


class Products(ProductsBase):
    id: int

    class Config:
        from_attributes: True
