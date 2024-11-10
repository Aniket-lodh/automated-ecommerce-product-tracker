import traceback
from typing import Optional, final
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas


def get_users(db: Session, single: bool = False, id: Optional[int] = None):
    try:
        if single and id is not None:
            return db.query(models.Users).filter(models.Users.id == id).first()
        elif not single:
            return db.query(models.Users).all()
        else:
            raise HTTPException(
                status_code=40,
                detail="ID must be provided when requesting a single user.",
            )
    except:
        db.rollback()
        traceback.print_exc()


def create_user(db: Session, email: str = ""):
    try:
        user = models.Users(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        db.rollback()
        traceback.print_exc()
        return None
