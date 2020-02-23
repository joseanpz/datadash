import logging

from app.utils.logging import setup_logging
from app.dao.config import database

logger = logging.getLogger(__name__)


async def startup_dbconection():
    try:
        logger.info(f'connecting... to: {database.connurl}')

        await database.crea_pool()
        logger.info(f'Pool: {str(database.pool)}')
    except Exception as e:
        print(e)


async def shutdown_dbconnection():
    await database.close()


async def startup_setup_logging():
    setup_logging()
