
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL =  "postgresql+asyncpg://postgres:982001@localhost:5432/solvv"

# Async engine
#engine = create_async_engine(DATABASE_URL, echo=True, future=True)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


from sqlalchemy import create_engine
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  
logging.getLogger("sqlalchemy.dialects").setLevel(logging.INFO)  

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

# Dependency
async def get_db():
    async with async_session() as session:
        yield session