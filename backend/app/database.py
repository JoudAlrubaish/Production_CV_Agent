from sqlalchemy import create_engine #engine means SQLAlchemy connection point to PostgreSQL 
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from backend.app.config import settings #to get .env setting information 

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(  #session to use for perform database operations
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db(): #used by FastAPI endpoints
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()