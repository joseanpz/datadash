from typing import Optional

from dataclasses import dataclass

from app.dao.config import database


@dataclass
class User:
    email: str
    hashed_password: str
    id: int = None
    is_active: bool = True
    is_superuser: bool = False
    full_name: str = None    

    async def create(self):
        print('meh')
        cursor = await database.pool.acquire()
        try:
            self.id = await cursor.fetchval(self.create_query)
        finally:
            await database.pool.release(cursor)
    
    async def get(self):
        cursor = await database.pool.acquire()
        try:
            record = await cursor.execute(self.getid_query)
            print(record)
        finally:
            await database.pool.release(cursor)
        # query = users.select(text(f"username = '{username}'"))
        # resp = await db.fetch_one(query)
        # if resp:
        #     return DBUser(**resp._row)

    async def update(self):
        cursor = await database.pool.acquire()
        try:
            record = await cursor.execute(self.update_query)
            print(record)
        finally:
            await database.pool.release(cursor)

    # def authenticate(self, password: str):
    #     user = self.get_by_email(db_session, email=email)
    #     if not user:
    #         return None
    #     if not verify_password(password, user.hashed_password):
    #         return None
    #     return user

    @property
    def create_query(self):
        return f"INSERT INTO users (email, hashed_password, is_active, is_superuser, full_name)" \
               f"VALUES ('{self.email}', '{self.hashed_password}', {self.is_active}, {self.is_superuser}, '{self.full_name}') " \
               "RETURNING id"
    
    @property
    def update_query(self):
        return f"UPDATE users SET full_name={self.full_name} hashed_password={self.hashed_password} " \
               f"WHERE id={self.id};"

    @property
    def getid_query(self, id):
        return f"SELECT id, email, full_name FROM users " \
               f"WHERE id={self.id}"
