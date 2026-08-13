
from datetime import datetime #to define when the model generate the prediction

from pydantic import BaseModel, ConfigDict

class TopPrediction(BaseModel): #output best k prediction candidate 
    class_name: str
    probability: float


class PredictionResponse(BaseModel): #what FastAPI will output at the end 
    id: int
    image_name: str
    predicted_class: str
    confidence: float
    top_k_predictions: list[TopPrediction]
    inference_ms: float
    model_version: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatsResponse(BaseModel): #used when request Frontend or Agent
    total_predictions: int
    class_distribution: dict[str, int]
    average_confidence: float


class ModelInfoResponse(BaseModel): #what model currently response 
    model_name: str
    model_version: str
    classes: list[str]
    input_size: list[int]
    deployment_status: str