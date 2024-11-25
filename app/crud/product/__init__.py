from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional, final
from fastapi import HTTPException
import models
from datetime import datetime
from crud.schemas import ProductCreate, TrackedProductsCreate


def get_product(
    db: Session,
    product_url: Optional[str] = None,
    product_name: Optional[str] = None,
    searchId: Optional[str] = None,
):
    try:
        if not searchId:
            if not product_name or not product_url:
                raise Exception(
                    "Both product name and url cannot be empty to fetch a product."
                )
            existing_product = (
                db.query(models.Products)
                .filter(
                    or_(
                        models.Products.name == product_name,
                        models.Products.url == product_url,
                    )
                )
                .first()
            )
            if existing_product:
                return existing_product
        else:
            existing_product_by_id = (
                db.query(models.Products)
                .filter(models.Products.id == int(searchId))
                .first()
            )
            if existing_product_by_id:
                return existing_product_by_id
        return None
    except Exception as e:
        raise Exception(str(e))


def add_product(db: Session, product_payload: ProductCreate):
    try:
        existing_prodcuct = get_product(
            db=db, product_name=product_payload.name, product_url=product_payload.url
        )
        if existing_prodcuct:
            return existing_prodcuct

        new_added_product = models.Products(**product_payload.model_dump())
        db.add(new_added_product)
        db.commit()
        db.refresh(new_added_product)
        return new_added_product
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def fetch_product(db: Session, id: int = None, single: bool = False):

    if single and not id:
        raise Exception("ID must be provided when requesting a single product.")

    try:
        if single and id is not None:
            product = db.query(models.Products).filter(models.Products.id == id).first()
            if product is None:
                raise Exception(f"No product found with ID {id}.")
            return product
        elif not single:
            products = db.query(models.Products).all()
            if not products:
                raise Exception("No products found.")
            return products
        else:
            raise Exception("Error fetching product / products, please try again later")
    except Exception as e:
        raise Exception(str(e))


def add_tracked_product(db: Session, product_payload: TrackedProductsCreate):
    try:
        existing_product = get_product(db=db, searchId=product_payload.product_id)
        if not existing_product:
            raise Exception(
                "No product found with the given product id, please try again later."
            )

        new_added_tracked_product = models.TrackedProducts(
            **product_payload.model_dump()
        )
        db.add(new_added_tracked_product)
        db.commit()
        db.refresh(new_added_tracked_product)
        return new_added_tracked_product
    except Exception as e:
        db.rollback()
        raise Exception(str(e))
