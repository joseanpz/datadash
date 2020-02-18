from app.utils.logging import setup_logging
from app.dao.config import database


async def startup_dbconection():
    try:
        await database.crea_pool()
    except Exception as e:
        print(e)


async def shutdown_dbconnection():
    await database.close()


async def startup_setup_logging():
    setup_logging()
