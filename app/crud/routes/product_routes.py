import traceback
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Users
from helpers import insert_otp
from database import get_db
from crud import add_product, fetch_product
from crud.schemas import ProductCreate
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

product_routes = APIRouter(prefix="/product", tags=["Product"])


@product_routes.post("/")
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    try:
        added_product = add_product(db=db, product_payload=data)
        serialized_product = jsonable_encoder(added_product)

        return JSONResponse(
            content={
                "status": 200,
                "message": "Product added successfully.",
                "body": serialized_product,
            },
        )
    except:
        print("error in /product")
        traceback.print_exc()
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating product, please try again later",
        )


@product_routes.get("/")
def get_products(
    id: Optional[int] = None, single: bool = False, db: Session = Depends(get_db)
):
    try:
        products = fetch_product(id=id, single=single, db=db)
        serialized_products = jsonable_encoder(products)

        return JSONResponse(
            content={
                "status": 200,
                "message": f"API ran successfully",
                "body": serialized_products,
            },
        )
    except Exception as e:
        print("error in /product")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
