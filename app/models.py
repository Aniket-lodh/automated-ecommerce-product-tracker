from sqlalchemy import DECIMAL, TIMESTAMP, Boolean, Column, String, Integer
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, autoincrement=False, primary_key=False, index=True)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, autoincrement=False, index=True)
    url = Column(String, autoincrement=False, index=True)
    price = Column(DECIMAL, autoincrement=False, index=True)
    availability = Column(Boolean, autoincrement=False, index=True)
    last_checked = Column(TIMESTAMP, autoincrement=False, index=True)
