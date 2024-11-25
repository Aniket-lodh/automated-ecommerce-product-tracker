import traceback
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

# from helpers import confirm_otp
import models


def get_user(
    db: Session, searchEmail: Optional[str] = None, searchId: Optional[str] = None
):
    try:
        if not searchId and not searchEmail:
            raise Exception("SearchId and searchEmail both cannot be empty")
        existing_user = (
            db.query(models.Users)
            .filter(or_(models.Users.id == searchId, models.Users.email == searchEmail))
            .first()
        )
        return existing_user
    except Exception as e:
        Exception(str(e))


def fetch_users(db: Session, single: bool = False, id: Optional[int] = None):
    if single and not id:
        raise Exception("ID must be provided when requesting a single user.")
    try:
        if single and id is not None:
            existing_user = get_user(db=db, searchId=id)
            # user = db.query(models.Users).filter(models.Users.id == id).first()
            if existing_user is None:
                raise Exception(f"No user found with ID {id}.")
            return existing_user
        elif not single:
            users = db.query(models.Users).all()
            if not users:
                raise Exception("No users found.")
            return users
        else:
            raise Exception("Invalid parameters for fetching users.")
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def verify_user(db: Session, email: str = ""):
    try:
        existing_user = get_user(db=db, searchEmail=email)
        if not existing_user:
            raise Exception("User doesnot exist, please sign up first!")

        return existing_user
    except Exception as e:
        raise Exception(str(e))


def add_user(db: Session, email: str = ""):
    try:
        existing_user = get_user(db=db, searchEmail=email)
        if existing_user:
            raise Exception("User aleady exists, please login.")
        user = models.Users(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise Exception(str(e))
