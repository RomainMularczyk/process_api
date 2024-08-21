import os
from pathlib import Path
from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}"
    f":{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

def db_session() -> Generator[Session, Any, Any]:
    """
    Open a database session.

    Yields
    ------
    Session
        A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
