import os
import logging

from asyncpg import create_pool
from asyncpg.pool import Pool
from dataclasses import dataclass, field

# base da datos
DATABASE_HOST = os.environ.get('DATABASE_HOST', '')
DATABASE_PORT = os.environ.get('DATABASE_PORT', 5432)
DATABASE_NAME = os.environ.get('DATABASE_NAME', '')
DATABASE_USER = os.environ.get('DATABASE_USER', '')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    f'postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

logger = logging.getLogger(__name__)


@dataclass
class PoolWrapper:
    connurl: str
    pool: Pool = field(init=False)

    async def crea_pool(self):
        try:
            self.pool = await create_pool(self.connurl)
        except Exception as e:
            logger.info(f'Ocurrio un error: {e}')

    async def close(self):
        await self.pool.close()


print(DATABASE_URL)
database = PoolWrapper(connurl=DATABASE_URL)
