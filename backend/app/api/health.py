#intiate health endpoint for FastAPI 
from fastapi import APIRouter
from sqlalchemy import text

from backend.app.database import engine
from backend.app.services.inference import load_model

router = APIRouter()

@router.get("/health")
def health_check():
    database_status = "healthy"
    model_status = "loaded"

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "unhealthy"

    try:
        load_model()
    except Exception:
        model_status = "not_loaded"

    return {
        "api": "healthy",
        "database": database_status,
        "model": model_status,
    }