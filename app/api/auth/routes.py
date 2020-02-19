from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.auth.dependencies import get_current_user
from app.api.auth.models import Token, Message
from app.api.utils.security import generate_password_reset_token, verify_password_reset_token
from app.api.user.models import UserCreate, UserResponse
from app.api.utils.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.core.security import get_password_hash
from app.dao.auth.schemas import UserAuth
from app.dao.user.schemas import UserRead as DBUserRead, UserReadByEmail as DBUserReadByEmail, \
    UserUpdateByEmail as DBUserUpdateByEmail

router = APIRouter()


@router.post("/auth/access-token", response_model=Token)
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


@router.post("/auth/test-token", response_model=UserResponse)
async def test_token(current_user: DBUserRead = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.post("/auth/password-recovery/{email}", response_model=Message)
async def recover_password(email: str):
    """
    Password Recovery
    """
    user = DBUserReadByEmail(email=email)
    await user.get()

    # if not user:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="The user with this username does not exist in the system.",
    #     )
    password_reset_token = generate_password_reset_token(email=email)
    # send_reset_password_email(
    #     email_to=user.email, email=email, token=password_reset_token
    # )
    return {"msg": f"Password recovery email sent: {password_reset_token}"}


@router.post("/auth/reset-password/", response_model=Message)
async def reset_password(token: str = Body(...), new_password: str = Body(...)):
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = DBUserUpdateByEmail(email=email)
    await user.get()
    # if not user:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="The user with this username does not exist in the system.",
    #     )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    await user.update()
    return {"msg": "Password updated successfully"}
