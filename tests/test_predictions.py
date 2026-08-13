#perform automated test for invalid uploads 
from fastapi.testclient import TestClient
from backend.app.main import app

#perform automated test for database insertion
from backend.app.database import SessionLocal
from backend.app.models import Prediction
from backend.app.services.prediction_service import save_prediction

client = TestClient(app)

#1.test for invalid uploads 
def test_invalid_image_type():
    files = {
        "image": (
            "document.txt",
            b"This is not an image.",
            "text/plain",
        )
    }

    response = client.post(
        "/api/v1/predict",
        files=files,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Unsupported image type. Use JPEG, PNG, or WEBP."
    )

#2.test for database insertion 
def test_database_insert():
    db = SessionLocal()

    prediction = None

    try:
        result = {
            "predicted_class": "happy",
            "confidence": 0.95,
            "top_predictions": [
                {
                    "class_name": "happy",
                    "probability": 0.95,
                },
                {
                    "class_name": "neutral",
                    "probability": 0.03,
                },
            ],
            "inference_ms": 30.5,
            "model_version": "test",
        }

        prediction = save_prediction(
            db=db,
            image_name="test_image.jpg",
            inference_result=result,
        )

        assert prediction.id is not None
        assert prediction.predicted_class == "happy"
        assert prediction.confidence == 0.95

    finally:
        if prediction is not None:
            stored_prediction = db.get(
                Prediction,
                prediction.id,
            )

            if stored_prediction is not None:
                db.delete(stored_prediction)
                db.commit()

        db.close()

#3.test for prediction history 
def test_prediction_history():
    db = SessionLocal()

    prediction = None

    try:
        result = {
            "predicted_class": "neutral",
            "confidence": 0.90,
            "top_predictions": [
                {
                    "class_name": "neutral",
                    "probability": 0.90,
                }
            ],
            "inference_ms": 25.0,
            "model_version": "test",
        }

        prediction = save_prediction(
            db=db,
            image_name="history_test.jpg",
            inference_result=result,
        )

        response = client.get("/api/v1/predictions")

        assert response.status_code == 200

        data = response.json()

        assert any(
            item["id"] == prediction.id
            for item in data
        )

    finally:
        if prediction is not None:
            stored_prediction = db.get(
                Prediction,
                prediction.id,
            )

            if stored_prediction is not None:
                db.delete(stored_prediction)
                db.commit()

        db.close()