#intiate model info endpoint for FastAPI 
from pathlib import Path
from fastapi import APIRouter
from backend.app.config import settings
from backend.app.schemas import ModelInfoResponse


router = APIRouter(
    prefix="/api/v1/model",
    tags=["Model"],
)


@router.get("", response_model=ModelInfoResponse)
def get_model_info():
    model_exists = Path(settings.model_path).exists() #check if model exist 
    #return model information 
    return {
        "model_name": "MobileNetV3 Small",
        "model_version": settings.model_version,
        "classes": [
            "neutral",
            "angry",
            "happy",
            "sad",
            "suprised",
            "tired",
        ],
        "input_size": [224, 224],
        "deployment_status": "loaded" if model_exists else "not_loaded",
    }