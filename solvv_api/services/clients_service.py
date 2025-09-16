from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from solvv_api.models.client import ClientModel
from solvv_api.schemas.client import ClientCreate, ClientUpdate
import traceback

async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 10):
    try:
        result = await db.execute(select(ClientModel).offset(skip).limit(limit))
        clients = result.scalars().all()
        return clients
    except Exception as e:
        print("ERROR inside get_clients:", e)
        print(traceback.format_exc())
        raise


async def get_client_by_id(db: AsyncSession, client_id: int):
    try:
        result = await db.execute(
            select(ClientModel).where(ClientModel.client_id == client_id)
        )
        client = result.scalar_one_or_none()

        if not client:
            print(f"⚠️ No client found with id {client_id}")
        else:
            print(f"✅ Found client: {client.client_name}")

        return client
    except Exception as e:
        print("ERROR inside get_client_by_id:", e)
        print(traceback.format_exc())
        raise


async def create_client(db: AsyncSession, client: ClientCreate):
    try:
        new_client = ClientModel(
            client_name=client.client_name,
            client_type=client.client_type,
            email=client.email,
            phone_number=client.phone_number,
            gst_number=client.gst_number,
            description=client.description,
        )
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        print(f"✅ Created new client with id {new_client.client_id}")
        return new_client
    except Exception as e:
        await db.rollback()
        print("ERROR inside create_client:", e)
        print(traceback.format_exc())
        raise


async def update_client(db: AsyncSession, client_id: int, client: ClientUpdate):
    try:
        existing = await get_client_by_id(db, client_id)
        if not existing:
            print(f"⚠️ Client with id {client_id} not found for update")
            return None

        # Update fields
        for field, value in client.dict(exclude_unset=True).items():
            setattr(existing, field, value)

        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        print(f"✅ Updated client {client_id}")
        return existing
    except Exception as e:
        await db.rollback()
        print("ERROR inside update_client:", e)
        print(traceback.format_exc())
        raise


async def delete_client(db: AsyncSession, client_id: int):
    try:
        existing = await get_client_by_id(db, client_id)
        if not existing:
            print(f"⚠️ Client with id {client_id} not found for delete")
            return None

        await db.delete(existing)
        await db.commit()
        print(f"🗑️ Deleted client {client_id}")
        return True
    except Exception as e:
        await db.rollback()
        print("ERROR inside delete_client:", e)
        print(traceback.format_exc())
        raise
