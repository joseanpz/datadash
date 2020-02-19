from typing import List

from pydantic import BaseModel


class GenericResponse(BaseModel):
    msg: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int = None
    scopes: List[str] = []
