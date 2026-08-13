#intiate health endpoint for FastAPI 
from fastapi import APIRouter
from sqlalchemy import text
from backend.app.database import engine


router = APIRouter()


@router.get("/health")
def health_check():
    database_status = "healthy" #test endpoint 

    try:
        with engine.connect() as connection: #test PostgreSQL
            connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "unhealthy"

    return {
        "api": "healthy",
        "database": database_status,
        "model": "not_loaded",
    }