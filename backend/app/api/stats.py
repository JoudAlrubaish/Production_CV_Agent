#intiate statistics endpoint for FastAPI 
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import Prediction
from backend.app.schemas import StatsResponse

router = APIRouter( 
    prefix="/api/v1/stats",
    tags=["Statistics"],
)

@router.get("", response_model=StatsResponse)
def get_prediction_statistics(
    db: Session = Depends(get_db),
):
    total_predictions = db.scalar(
        select(func.count(Prediction.id)) #count avillable predictions 
    ) or 0

    average_confidence = db.scalar(
        select(func.avg(Prediction.confidence)) #calculate avg confidence predictions in the table db 
    )

    class_counts = db.execute(
        select(
            Prediction.predicted_class,
            func.count(Prediction.id),
        )
        .group_by(Prediction.predicted_class) #group based on predictions classes 
    ).all()

    class_distribution = {
        class_name: count
        for class_name, count in class_counts
    }

    return {
        "total_predictions": total_predictions,
        "class_distribution": class_distribution,
        "average_confidence": float(average_confidence or 0.0),
    }