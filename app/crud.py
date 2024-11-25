import time
import traceback
from turtle import mode
from typing import Optional, final
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime


# TODO:// fix this
# TODO:// create separate route to add a product into db and a separate api to add a existing product into trackedProducts db
def create_tracked_products(db: Session, data: schemas.TrackedProductsCreate):
    try:
        # checking if user is valid
        valid_user = get_users(db, single=True, id=data.user_id)
        if valid_user and valid_user.id is not None and valid_user.email is not None:
            product = get_or_create_product(db=db, data=data)
            print(product)

            existing_tracked_product = (
                db.query(models.TrackedProducts)
                .filter(
                    models.TrackedProducts.product_id == product.id,
                    models.TrackedProducts.user_id == valid_user.id,
                )
                .first()
            )
            if existing_tracked_product:
                return existing_tracked_product

            tracked_product = models.TrackedProducts(
                target_price=data.target_price,
                notified=data.notified,
                product_id=product.id,
                user_id=valid_user.id,
            )
            db.add(tracked_product)
            db.commit()
            db.refresh(tracked_product)
            return tracked_product
        print(tracked_product)
    except:
        db.rollback()
        traceback.print_exc()
        return None
