from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import logging
import traceback


app = FastAPI(title="Solvv API", version="1.0")
templates = Jinja2Templates(directory="templates")

# Routers
from solvv_api.routers import mentor, client
app.include_router(mentor.router, prefix="/mentors", tags=["Mentors"])
app.include_router(client.router, prefix="/clients", tags=["Clients"])

# Database
from solvv_api.core.database import Base, engine

# Exception handlers
from solvv_api.exceptions.handlers import (
    client_not_found_handler,
    client_already_exists_handler,
    invalid_client_type_handler,
    database_connection_handler
)
from solvv_api.exceptions.custom_exceptions import (
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidClientTypeException,
    DatabaseConnectionException
)


@app.on_event("startup")
async def on_startup():
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
   
# Exception handlers
app.add_exception_handler(ClientNotFoundException, client_not_found_handler)
app.add_exception_handler(ClientAlreadyExistsException, client_already_exists_handler)
app.add_exception_handler(InvalidClientTypeException, invalid_client_type_handler)
app.add_exception_handler(DatabaseConnectionException, database_connection_handler)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()
    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled error: {exc}\n{error_trace}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )

# Root route
@app.get("/")
def root():
    return {"message": "API is running!"}

