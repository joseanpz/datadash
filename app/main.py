from fastapi import FastAPI

from app import config
from app.api.auth.routes import router as users_router
from app.utils.events import (shutdown_dbconnection, startup_dbconection,
                              startup_setup_logging)
from app.utils.exceptions import SomeException, some_exception_handler
from app.utils.middleware import UUIDMidleware, DBMidleware

app = FastAPI(
    title="Plataforma Analitica",
    description="Servicios de plataforma analitica",
    version=config.__VERSION__
)

# events handlers
app.add_event_handler('startup', startup_setup_logging)
app.add_event_handler('startup', startup_dbconection)
app.add_event_handler('shutdown', shutdown_dbconnection)

# exceptions
app.add_exception_handler(SomeException, some_exception_handler)

# middleware
app.add_middleware(UUIDMidleware)
app.add_middleware(DBMidleware)

# routes
app.include_router(users_router, prefix="", tags=["usuarios"])
