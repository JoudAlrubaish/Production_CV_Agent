#intiate FastAPI application with importing endpoints 
from fastapi import FastAPI
from backend.app.api.health import router as health_router
from backend.app.api.history import router as history_router
from backend.app.api.stats import router as stats_router
from backend.app.api.model_info import router as model_info_router
from backend.app.api.predictions import router as predictions_router

app = FastAPI( #creates the actual API application
    title="Face Emotion Classification API",
    version="1.0.0",
    description="Backend API for the Production Computer Vision Agent.",
)

app.include_router(health_router) #/health route we created in another file and attaches it to the main application
app.include_router(history_router) #history route we created in another file and attaches it to the main application
app.include_router(stats_router)#statistics route we created in another file and attaches it to the main application
app.include_router(model_info_router) #model info route we created in another file and attaches it to the main application
app.include_router(predictions_router)#prediction route we created in another file and attaches it to the main application

@app.get("/")
def root():
    return {
        "message": "Face Emotion Classification API is running"
    }