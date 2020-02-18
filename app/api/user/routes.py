from asyncpg import UniqueViolationError
from dataclasses import asdict
from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import Response

from app.api.user.models import UserCreate, UserResponse, UserUpdate
from app.api.auth.dependencies import get_current_active_user
from app.dao.user.schemas import UserRead as DBUserRead, UserDelete as DBUserDelete, UserUpdate as DBUserUpdate, \
    UserCreate as DBUserCreate

# from app.utils import send_new_account_email

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create(response: Response, request: Request, user_input: UserCreate,
                 current_user: DBUserRead = Depends(get_current_active_user)):
    """
    Create new user.
    """
    if current_user.is_superuser:
        dbuser = DBUserCreate(
            email=user_input.email,
            hashed_password=user_input.hashed_password,
            full_name=user_input.full_name
        )
        try:
            await dbuser.create()
            response.status_code = 201
        except UniqueViolationError as e:
            raise HTTPException(status_code=400, detail="A user with this email already exists.")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Unmanaged error.")
        return asdict(dbuser)
    else:
        raise HTTPException(status_code=401, detail='Unauthorized operation.')


@router.get("/users/{userid}", response_model=UserResponse)
async def retrieve(response: Response, request: Request, userid: int):
    dbuser = DBUserRead(id=userid)
    try:
        await dbuser.get()
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    return asdict(dbuser)


@router.put("/users/{userid}", response_model=UserResponse)
async def update(response: Response, request: Request, userid: int, user_input: UserUpdate):
    dbuser = DBUserUpdate(id=userid, hashed_password=user_input.password)
    try:
        await dbuser.get()
        dbuser.set(user_input)
        await dbuser.update()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return asdict(dbuser)


@router.delete("/users/{userid}")
async def delete(response: Response, request: Request, userid: int):
    dbuser = DBUserDelete(id=userid)
    try:
        await dbuser.delete()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"OK": 200}


@router.get("/users/me", response_model=UserResponse)
async def me(response: Response, request: Request, userid: int):
    dbuser = DBUserRead(id=userid)
    try:
        await dbuser.get()
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    return asdict(dbuser)