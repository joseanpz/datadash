from typing import Optional

from pydantic import BaseModel, Schema


# Shared properties
class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: str = None


class UserBaseInDB(UserBase):
    id: int = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int


class UserDB(UserResponse):    
    hashed_password: str
    id: int = None    


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserCreate):
    id: int = None


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str
