from re import A
from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    func,
)
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, autoincrement=False, primary_key=False, index=True)
    email_verified = Column(
        Boolean,
        autoincrement=False,
        primary_key=False,
        index=True,
        default=False,
        nullable=False,
    )
    logged_in = Column(
        Boolean,
        autoincrement=False,
        primary_key=False,
        index=True,
        default=False,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        autoincrement=False,
        nullable=False,
        index=True,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        autoincrement=False,
        nullable=True,
        index=True,
        default=None,
    )
    verified_at = Column(
        TIMESTAMP(timezone=True),
        autoincrement=False,
        nullable=True,
        index=True,
        default=None,
    )


class UsersSession(Base):
    __tablename__ = "session"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey(Users.id, ondelete="CASCADE"),
        autoincrement=False,
        nullable=False,
        index=True,
    )
    generated_otp = Column(
        Integer, autoincrement=False, primary_key=False, nullable=False, index=True
    )
    verified = Column(
        Boolean,
        default=False,
        autoincrement=False,
        nullable=False,
        index=True,
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        autoincrement=False,
        nullable=False,
        index=True,
    )
    verified_at = Column(
        TIMESTAMP(timezone=True),
        autoincrement=False,
        nullable=True,
        index=True,
        default=None,
    )


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, autoincrement=False, index=True)
    url = Column(String, autoincrement=False, index=True)
    price = Column(
        DECIMAL,
        autoincrement=False,
        index=True,
        nullable=False,
    )
    availability = Column(
        Boolean,
        autoincrement=False,
        index=True,
        nullable=False,
    )
    last_checked = Column(
        TIMESTAMP(timezone=True),
        autoincrement=False,
        index=True,
        nullable=True,
        default=None,
    )


class TrackedProducts(Base):
    __tablename__ = "tracked_products"

    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(Users.id, ondelete="CASCADE"),
        index=True,
        autoincrement=False,
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey(Products.id, ondelete="CASCADE"),
        index=True,
        autoincrement=False,
        nullable=False,
    )
    target_price = Column(String, nullable=False, autoincrement=False, index=True)
    notified = Column(
        Boolean, default=False, autoincrement=False, nullable=False, index=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        autoincrement=False,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product"),
    )
