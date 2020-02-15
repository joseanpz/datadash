from starlette.requests import Request
from starlette.responses import JSONResponse


class SomeException(Exception):
    def __init__(self, folio: str):
        self.folio = folio


def some_exception_handler(request: Request, exc: SomeException):
    return JSONResponse(
        status_code=418,
        content={
            "trace_id": request.state.automata_uuid,
            "message": "Some error has ocurred"
        },
    )
