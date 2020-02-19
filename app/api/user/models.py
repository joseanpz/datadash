from typing import Optional

from pydantic.main import BaseModel

from app.core.security import get_password_hash


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: str = None


class UserCreate(UserBase):
    password: str

    @property
    def hashed_password(self):
        return get_password_hash(self.password)


class UserResponse(UserBase):
    id: int


class UserBaseInDB(UserBase):
    id: int = None


class UserUpdate(UserBaseInDB):
    email: str = None
    password: Optional[str] = None

    @property
    def hashed_password(self):
        return None if self.password is None else get_password_hash(self.password)
