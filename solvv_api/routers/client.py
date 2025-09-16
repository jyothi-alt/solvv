from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from solvv_api.core.database import get_db
from solvv_api.schemas.client import ClientCreate, ClientUpdate, ClientOut
from solvv_api.services import clients_service

router = APIRouter(prefix="/solvv/admin", tags=["Clients"])

@router.get("/clients", response_model=List[ClientOut])
async def list_clients(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await clients_service.get_clients(db, skip=skip, limit=limit)


@router.get("/client/{client_id}", response_model=ClientOut)
async def get_client(client_id: int, db: AsyncSession = Depends(get_db)):
    try:
        client = await clients_service.get_client_by_id(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.post("/client", response_model=ClientOut)
async def create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await clients_service.create_client(db, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.put("/client/{client_id}", response_model=ClientOut)
async def update_client(client_id: int, client: ClientUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated = await clients_service.update_client(db, client_id, client)
        if not updated:
            raise HTTPException(status_code=404, detail="Client not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.delete("/client/{client_id}")
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted = await clients_service.delete_client(db, client_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Client not found")
        return {"detail": "Client deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
