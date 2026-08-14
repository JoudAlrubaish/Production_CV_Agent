#intiate FastAPI application with importing endpoints 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.api.history import router as history_router
from backend.app.api.stats import router as stats_router
from backend.app.api.model_info import router as model_info_router
from backend.app.api.predictions import router as predictions_router

from backend.app.config import settings
from backend.app.database import Base, engine
from backend.app import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Face Emotion Classification API",
    version="1.0.0",
    description="Backend API for the Production Computer Vision Agent.",
)


origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(history_router)
app.include_router(stats_router)
app.include_router(model_info_router)
app.include_router(predictions_router)


@app.get("/")
def root():
    return {
        "message": "Face Emotion Classification API is running"
    }