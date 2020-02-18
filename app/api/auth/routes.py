from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.auth.models import Token
from app.api.utils.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.dao.auth.schemas import UserAuth

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserAuth(email=form_data.username, password=form_data.password).authenticate()
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.email, "user_id": user.id, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
