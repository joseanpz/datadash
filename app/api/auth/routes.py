from typing import List

from dataclasses import asdict
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
# from sqlalchemy.orm import Session

from app.api.auth.models import UserResponse, UserCreate
from app.dao.auth.schemas import User as DBUser
# from app import crud
# from app.api.utils.db import get_db
# from app.api.utils.security import get_current_active_superuser, get_current_active_user
# from app.core import config
# from app.models.user import User as DBUser
# from app.schemas.user import User, UserCreate, UserUpdate
# from app.utils import send_new_account_email

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create(response: Response, request: Request, user_inp: UserCreate):
    """
    Create new user.
    """
    dbuser = DBUser(
        email=user_inp.email, 
        hashed_password=user_inp.password, 
        full_name=user_inp.full_name
    )
    await dbuser.create()
    return asdict(dbuser)
    # if user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="The user with this username already exists in the system.",
    #      )
    # user = crud.user.create(db, obj_in=user_in)
    # if config.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    # return user
