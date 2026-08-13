
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.app.models import Prediction

"""save_prediction will take the prediction from the model and covert it to row in PostgreSQL"""

def save_prediction( 
    db: Session,
    image_name: str,
    inference_result: dict,
) -> Prediction:

    prediction = Prediction(
        image_name=image_name,
        predicted_class=inference_result["predicted_class"],
        confidence=inference_result["confidence"],
        top_k_predictions=inference_result["top_predictions"],
        inference_ms=inference_result["inference_ms"],
        model_version=inference_result["model_version"],
    )

    try:
        db.add(prediction)
        db.commit()
        db.refresh(prediction) #to read last version 

        return prediction

    except SQLAlchemyError:
        db.rollback() # in case of database faillure transaction rollback again 
        raise