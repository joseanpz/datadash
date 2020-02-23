import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.utils.security import SECRET_KEY, ALGORITHM
from app.api.auth.models import TokenData
from app.dao.user.schemas import UserRead

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/auth/access-token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


async def get_current_user(security_scopes: SecurityScopes,
                           token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        # verify access token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, user_id=user_id)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    # user is (almost) authenticated
    user = UserRead(id=token_data.user_id)
    try:
        await user.get()
    except Exception as e:
        credentials_exception.detail = str(e)
        raise credentials_exception

    # validate scopes (dummy?)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: UserRead = Security(get_current_user, scopes=["me"])):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user