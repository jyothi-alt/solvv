from fastapi import Request
from fastapi.responses import JSONResponse
from .custom_exceptions import (
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidClientTypeException,
    DatabaseConnectionException
)

async def client_not_found_handler(request: Request, exc: ClientNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": request.url.path}
    )

async def client_already_exists_handler(request: Request, exc: ClientAlreadyExistsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def invalid_client_type_handler(request: Request, exc: InvalidClientTypeException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def database_connection_handler(request: Request, exc: DatabaseConnectionException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
