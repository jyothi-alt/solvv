from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:982001@localhost:5432/solvv"

# Remove 'connect_args' for PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
