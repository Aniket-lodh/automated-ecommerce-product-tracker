from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    email: str
    email_verified: bool
    logged_in: bool
    updated_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None


class UsersReqModel(BaseModel):
    email: str
    pass


class UsersSQLALModel(UsersBase):
    id: int

    class Config:
        from_attributes = True
