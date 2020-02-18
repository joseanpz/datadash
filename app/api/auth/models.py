from typing import List

from app.api.user.models import UserCreate, UserResponse, UserBaseInDB
from pydantic import BaseModel


# Shared properties


# Properties to receive via API on creation


class UserDB(UserResponse):
    hashed_password: str
    id: int = None    


# Properties to receive via API on update


# Additional properties to return via API
class User(UserCreate):
    id: int = None


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int = None
    scopes: List[str] = []
