import logging
import time

from asyncpg import UniqueViolationError
from asyncpg.protocol.protocol import Record
from dataclasses import dataclass

from app.api.user.models import UserUpdate as APIUserUpdate
from app.dao.config import database

logger = logging.getLogger(__name__)


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
            start_time = time.time()
            record = await cursor.fetchrow(self.get_query)
            process_time = time.time() - start_time
            logger.info(f'Database time processing (get): {str(process_time)}')
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
class UserReadByEmail(UserRead):
    id: int = None
    email: str = ...

    @property
    def get_query(self):
        return f"SELECT * FROM users WHERE email={self.email} "


@dataclass
class UserDelete(UserRead):

    async def delete(self):
        cursor = await database.pool.acquire()
        try:
            start_time = time.time()
            await cursor.execute(self.delete_query)
            process_time = time.time() - start_time
            logger.info(f'Database time processing (delete): {str(process_time)}')
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
            start_time = time.time()
            await cursor.execute(self.update_query)
            process_time = time.time() - start_time
            logger.info(f'Database time processing (update): {str(process_time)}')
        finally:
            await database.pool.release(cursor)

    def set(self, this: APIUserUpdate):
        if getattr(this, 'email', None) is not None:
            self.email = this.email
        if getattr(this, 'hashed_password', None) is not None:
            self.hashed_password = this.hashed_password
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
        query = f"SET full_name='{self.full_name}', is_active={self.is_active}, " \
                f"is_superuser={self.is_superuser}"
        if self.hashed_password is not None:
            query = f"{query}, hashed_password='{self.hashed_password}'"
        return query


@dataclass
class UserUpdateByEmail(UserUpdate):

    @property
    def update_query(self):
        return f"UPDATE users {self.set_query} WHERE email={self.email};"

    @property
    def set_query(self):
        return f'SET hashed_password={self.hashed_password}'


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
            start_time= time.time()
            self.id = await cursor.fetchval(self.create_query)
            process_time = time.time() - start_time
            logger.info(f'Database time processing (create): {str(process_time)}')
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