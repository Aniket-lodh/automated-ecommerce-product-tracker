from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UsersSessionBase(BaseModel):
    user_id: int
    generated_otp: int
    verified: bool
    verified_at: Optional[datetime] = None


class UsersSessionReqModel(BaseModel):
    user_email: str
    generated_otp: int
    pass


class UsersSessionSQLALModel(UsersSessionBase):
    id: int

    class Config:
        from_attributes: True
