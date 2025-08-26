from fastapi import HTTPException, status

class ClientNotFoundException(HTTPException):
    def __init__(self, client_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found."
        )

class ClientAlreadyExistsException(HTTPException):
    def __init__(self, client_name: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Client with name '{client_name}' already exists."
        )

class InvalidClientTypeException(HTTPException):
    def __init__(self, client_type: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid client type: {client_type}. Must be 'retail' or 'corporate'."
        )

class DatabaseConnectionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed."
        )
