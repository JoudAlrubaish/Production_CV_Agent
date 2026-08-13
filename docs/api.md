# API Contract

## Health

GET /health

Checks:
- API
- Database
- Model

---

## Model Information

GET /api/v1/model

Returns information about the deployed model.

---

## Predict Emotion

POST /api/v1/predict

Input:

multipart/form-data

image=<file>

Example output:

{
  "predicted_class": "happy",
  "confidence": 0.9412,
  "top_predictions": [
    {
      "class_name": "happy",
      "probability": 0.9412
    }
  ],
  "inference_ms": 37.5,
  "model_version": "1.0.0"
}

---

## Prediction History

GET /api/v1/predictions

Returns stored predictions.

---

## Single Prediction

GET /api/v1/predictions/{prediction_id}

Returns one prediction.

---

## Statistics

GET /api/v1/stats

Returns:
- Total predictions
- Class distribution
- Average confidence