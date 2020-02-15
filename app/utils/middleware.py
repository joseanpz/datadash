import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.dao.config import database

logger = logging.getLogger(__name__)


class UUIDMidleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request.state.automata_uuid = uuid.uuid4()
        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        log = logging.LoggerAdapter(logger, {'trace_uuid': request.state.automata_uuid})
        log.info(f'Datos de cabecera de respuesta: {response.raw_headers}')
        return response


class DBMidleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.db = database
        response = await call_next(request)
        return response