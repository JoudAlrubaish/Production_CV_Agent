#intiate prediction and prediction id endpoints for FastAPI 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import Prediction
from backend.app.schemas import PredictionResponse

router = APIRouter(prefix="/api/v1/predictions",tags=["Predictions"]) #to make every endpoint in this file starts with /api/v1/predictions

@router.get("", response_model=list[PredictionResponse])#endpoint returns a list of predictions
def get_prediction_history(db: Session = Depends(get_db)): #connect the endpoint to the database function 
    statement = (
        select(Prediction)
        .order_by(Prediction.created_at.desc())  #every prediction must follow our PredictionResponse schema 
    )

    predictions = db.scalars(statement).all() 

    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse) 
def get_prediction_by_id( #ask about prediction using threre primary key id 
    prediction_id: int,
    db: Session = Depends(get_db),
):
    prediction = db.get(Prediction, prediction_id)

    if prediction is None: #if the prediction is missing 
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    return prediction