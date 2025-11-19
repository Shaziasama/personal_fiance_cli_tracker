# app/database/engine.py
import os
import contextlib
from typing import Generator

from sqlmodel import create_engine, Session, SQLModel

from app.models.transaction import Transaction # Importing to ensure tables are created
from app.models.budget import Budget # Importing to ensure tables are created

# Database URL from environment variable or default SQLite file
DATABASE_URL = os.getenv("DB_URL", "sqlite:///./database.db")

engine = create_engine(DATABASE_URL, echo=True) # echo=True for debugging SQL queries


def create_db_and_tables():
    """Creates all SQLModel tables."""
    SQLModel.metadata.create_all(engine)

@contextlib.contextmanager
def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session

