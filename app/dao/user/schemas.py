from asyncpg import UniqueViolationError
from asyncpg.protocol.protocol import Record
from dataclasses import dataclass

from app.api.user.models import UserUpdate as APIUserUpdate
from app.dao.config import database


@dataclass
class BaseUser:
    id: int = None
    is_active: bool = True
    is_superuser: bool = False
    full_name: str = None


@dataclass
class UserRead(BaseUser):
    id: int = ...
    email: str = None

    async def get(self):
        cursor = await database.pool.acquire()
        try:
            record = await cursor.fetchrow(self.get_query)
            self.setfromdb(record)
        finally:
            await database.pool.release(cursor)

    def setfromdb(self, record: Record):
        self.email = record['email']
        self.full_name = record['full_name']
        self.is_active = record['is_active']
        self.is_superuser = record['is_superuser']

    @property
    def get_query(self):
        return f"SELECT * FROM users WHERE id={self.id} "


@dataclass
class UserDelete(UserRead):

    async def delete(self):
        cursor = await database.pool.acquire()
        try:
            await cursor.execute(self.delete_query)
        finally:
            await database.pool.release(cursor)

    @property
    def delete_query(self):
        return f"DELETE  FROM users WHERE {self.condition}"

    @property
    def condition(self):
        return f"id={self.id}"


@dataclass
class UserUpdate(UserRead):
    hashed_password: str = None

    async def update(self):
        cursor = await database.pool.acquire()
        try:
            record = await cursor.execute(self.update_query)
            print(record)
        finally:
            await database.pool.release(cursor)

    def set(self, this: APIUserUpdate):
        if getattr(this, 'email', None) is not None:
            self.email = this.email
        if getattr(this, 'full_name', None) is not None:
            self.full_name = this.full_name
        if getattr(this, 'is_active', None) is not None:
            self.is_active = this.is_active
        if getattr(this, 'is_superuser', None) is not None:
            self.is_superuser = this.is_superuser

    @property
    def update_query(self):
        return f"UPDATE users {self.set_query} WHERE id={self.id};"

    @property
    def set_query(self):
        return f"SET full_name='{self.full_name}', is_active={self.is_active}, is_superuser={self.is_superuser}"


@dataclass
class UserUpdateMe(UserUpdate):

    @property
    def set_query(self):
        return f'SET full_name={self.full_name} hashed_password={self.hashed_password}'


@dataclass
class UserCreate(BaseUser):
    email: str = ...
    hashed_password: str = ...

    async def create(self):
        cursor = await database.pool.acquire()
        try:
            self.id = await cursor.fetchval(self.create_query)
        except UniqueViolationError as e:
            print(e)
            raise e
        finally:
            await database.pool.release(cursor)

    @property
    def create_query(self):
        return f"INSERT INTO users (email, hashed_password, is_active, is_superuser, full_name)" \
               f"VALUES ('{self.email}', '{self.hashed_password}', {self.is_active}, {self.is_superuser}, '{self.full_name}') " \
               "RETURNING id"