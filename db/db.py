import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .config import DB_HOST, DB_PASSWORD, DB_USER, DB_NAME

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

@contextmanager
def get_db():
    """
    Dependency that provides a database session.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

