# main.py

from fastapi import FastAPI
from solvv_api.core.database import Base, engine
from solvv_api.routers import clients
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

# Create all tables if not exists
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Solvv API", version="1.0")

# Include routers
app.include_router(clients.router)

# Add custom exception handlers
app.add_exception_handler(ClientNotFoundException, client_not_found_handler)
app.add_exception_handler(ClientAlreadyExistsException, client_already_exists_handler)
app.add_exception_handler(InvalidClientTypeException, invalid_client_type_handler)
app.add_exception_handler(DatabaseConnectionException, database_connection_handler)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Solvv API!"}
