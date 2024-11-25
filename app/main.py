import time
import traceback, models
from helpers import confirm_otp, insert_otp
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import engine, LocalSession, get_db
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from crud import (
    add_product,
    fetch_users,
    add_user,
    fetch_product,
    add_tracked_product,
    verify_user,
)
from crud.schemas import (
    UsersReqModel,
    ProductCreate,
    TrackedProductsCreate,
    UsersSessionReqModel,
)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def server():
    return JSONResponse(content={"message": "welcome to the server"})


@app.get("/user")
def get_users(
    id: Optional[int] = None, single: bool = False, db: Session = Depends(get_db)
):
    try:
        users = fetch_users(db=db, id=id, single=single)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/user/login")
def log_in(user_request: UsersReqModel, db: Session = Depends(get_db)):
    try:
        user = verify_user(db=db, email=user_request.email)
        if user is None:
            raise Exception("Couldnt log in, please try again later!")

        inserted_otp = insert_otp(user, db)
        if inserted_otp is None:
            raise Exception("Failed to generate otp, please try again later!")
        return user
    except Exception as e:
        print("error in /user/")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/user/register")
def create_user(user_request: UsersReqModel, db: Session = Depends(get_db)):
    try:
        user = add_user(db=db, email=user_request.email)
        if user is None:
            raise Exception("Error creating user in the database.")
        inserted_otp = insert_otp(user, db)
        if inserted_otp is None:
            raise Exception("Failed to generate otp, please try again later!")
        return user
    except Exception as e:
        print("error in /user/")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/otp/verify")
def verify_otp(request_body: UsersSessionReqModel, db: Session = Depends(get_db)):
    try:
        verified_otp = confirm_otp(request_body, db)
        if not verified_otp:
            raise Exception("Error verifying otp, please try again later!")
        return JSONResponse(
            content={
                "message": "Verified otp, redirecting to home page...",
                "status": 200,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/product")
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    try:
        added_product = add_product(db=db, product_payload=data)
        return added_product
    except:
        print("error in /product")
        traceback.print_exc()
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating product, please try again later",
        )


@app.get("/product")
def get_products(
    id: Optional[int] = None, single: bool = False, db: Session = Depends(get_db)
):
    try:
        products = fetch_product(id=id, single=single, db=db)
        return products
    except Exception as e:
        print("error in /product")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/track-product")
def track_product(data: TrackedProductsCreate, db: Session = Depends(get_db)):
    try:
        tracked_products = add_tracked_product(db=db, payload_data=data)
        return tracked_products
    except Exception as e:
        print("error in /track-products/")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                str(e)
                if str(e)
                else "Error adding product to track, please try again later!"
            ),
        )


# TODO: Implement cookie feature for user continious session.
# Maybe store user cookie in db


@app.middleware("http")
async def add_process_time_header(req: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(req)
    process_time = time.perf_counter() - start_time
    response.headers["X-process-Time"] = str(process_time)
    return response
