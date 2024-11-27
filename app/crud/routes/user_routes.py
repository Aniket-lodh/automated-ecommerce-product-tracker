from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Users
from helpers import insert_otp
from database import get_db
from crud import (
    fetch_users,
    add_user,
    verify_user,
)
from crud.schemas import UsersReqModel
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

user_routes = APIRouter(prefix="/user", tags=["User"])


@user_routes.get("/")
def get_users(
    id: Optional[int] = None, single: bool = False, db: Session = Depends(get_db)
):
    try:
        users = fetch_users(db=db, id=id, single=single)
        serialized_users = jsonable_encoder(users)

        return JSONResponse(
            content={
                "status": 200,
                "message": f"API ran successfully",
                "body": serialized_users,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_routes.post("/login")
def log_in(user_request: UsersReqModel, db: Session = Depends(get_db)):
    try:
        user = verify_user(db=db, email=user_request.email)
        if user is None:
            raise Exception("Couldnt log in, please try again later!")

        inserted_otp = insert_otp(user, db)
        if inserted_otp is None:
            raise Exception("Failed to generate otp, please try again later!")

        return JSONResponse(
            content={
                "message": f"OTP has been sent to {user.email}",
                "status": 200,
            },
        )
    except Exception as e:
        print("error in /user/")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_routes.post("/register")
def create_user(user_request: UsersReqModel, db: Session = Depends(get_db)):
    try:
        user = add_user(db=db, email=user_request.email)
        if user is None:
            raise Exception("Error creating user in the database.")

        inserted_otp = insert_otp(user, db)
        if inserted_otp is None:
            raise Exception("Failed to generate otp, please try again later!")

        return JSONResponse(
            content={
                "message": f"OTP has been sent to {user.email}",
                "status": 200,
            },
        )
    except Exception as e:
        print("error in /user/")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
