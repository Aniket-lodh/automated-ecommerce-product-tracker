import traceback
from typing import List, Optional

from fastapi.responses import JSONResponse
import models, schemas, crud
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, LocalSession, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def server():
    return JSONResponse(content={"message": "welcome to the server"})


@app.get("/users", response_model=List[schemas.Users])
def get_users(
    id: Optional[int] = None,
    single: bool = False,
    db: Session = Depends(get_db),
):
    try:
        users = crud.get_users(db=db, id=id, single=single)
        return users
    except:
        print("error in /users/")
        traceback.print_exc()


@app.post("/user", response_model=schemas.Users)
def create_item(user_request: schemas.UsersBase, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db=db, email=user_request.email)
        if user is None:
            raise Exception("Error creating user in the database.")
        return user
    except Exception as e:
        print("error in /user/")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
