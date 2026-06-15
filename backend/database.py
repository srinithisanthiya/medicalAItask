from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import settings


class Base(DeclarativeBase):
    pass


def _sqlite_url(url: str) -> str:
    if url.startswith("sqlite:///./"):
        db_path = Path(url.replace("sqlite:///./", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return url


engine = create_engine(
    _sqlite_url(settings.database_url),
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
