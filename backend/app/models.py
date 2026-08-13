
from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database import Base


class Prediction(Base): #describes prediction table that came from the predictive model
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    image_name: Mapped[str] = mapped_column(String, nullable=False)

    predicted_class: Mapped[str] = mapped_column( String, nullable=False)

    confidence: Mapped[float] = mapped_column(Float, nullable=False )

    top_k_predictions: Mapped[dict | list] = mapped_column(JSON, nullable=False )

    inference_ms: Mapped[float] = mapped_column(Float, nullable=False)

    model_version: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,nullable=False)


#example output 
#Prediction(
#  image_name="face1.jpg",
#  predicted_class="happy",
#  confidence=0.94,
#  top_k_predictions=[
#  {"class_name": "happy", "probability": 0.94},
#  {"class_name": "neutral", "probability": 0.04},
#  ],
#   inference_ms=35.2,
#   model_version="1.0.0",
#)