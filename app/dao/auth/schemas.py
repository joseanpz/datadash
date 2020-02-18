from asyncpg import Record
from dataclasses import dataclass

from app.core.security import verify_password
from app.dao.config import database


@dataclass
class UserAuth:
    id: int = None
    email: str = ...
    password: str = ...
    hashed_password: str = None

    async def authenticate(self):
        await self.get()
        if not verify_password(self.password, self.hashed_password):
            return False
        return self

    async def get(self):
        cursor = await database.pool.acquire()
        try:
            record = await cursor.fetchrow(self.getemail_query)
            self.set(record)
        finally:
            await database.pool.release(cursor)

    def set(self, record: Record):
        self.id = record['id']
        self.hashed_password = record['hashed_password']

    @property
    def getemail_query(self):
        return f"SELECT * FROM users WHERE email='{self.email}'"
