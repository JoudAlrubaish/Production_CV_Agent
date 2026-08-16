# FastAPI API Documentation

## Base URL

Local:

```text
http://127.0.0.1:8000
```

Production:

```text
<FASTAPI_PRODUCTION_URL>
```

Swagger:

```text
/docs
```

---

# 1. Health Check

## Request

```http
GET /health
```

## Purpose

Checks:

```text
FastAPI
PostgreSQL
Computer Vision model
```

Example response:

```json
{
  "api": "healthy",
  "database": "healthy",
  "model": "loaded"
}
```

The API itself may still be reachable even if the database or model reports an unhealthy state.

---

# 2. Prediction

## Request

```http
POST /api/v1/predict
```

Content type:

```text
multipart/form-data
```

Field:

```text
image
```

Example using curl:

```bash
curl -X POST \
  -F "image=@face.jpg" \
  http://127.0.0.1:8000/api/v1/predict
```

---

## Supported Formats

```text
image/jpeg
image/png
image/webp
```

Maximum size:

```text
5 MB
```

---

## Validation Flow

```text
Receive upload
 ↓
Validate MIME type
 ↓
Read bytes
 ↓
Check size
 ↓
Verify actual image
 ↓
Run model
 ↓
Sanitize filename
 ↓
Store prediction
 ↓
Return stored record
```

---

## Successful Response

```json
{
  "id": 1,
  "image_name": "face.jpg",
  "predicted_class": "happy",
  "confidence": 0.9412,
  "top_k_predictions": [
    {
      "class_name": "happy",
      "probability": 0.9412
    },
    {
      "class_name": "neutral",
      "probability": 0.04
    },
    {
      "class_name": "sad",
      "probability": 0.0188
    }
  ],
  "inference_ms": 32.1,
  "model_version": "1.0.0",
  "created_at": "2026-08-15T12:00:00"
}
```

---

## Possible Errors

### Unsupported Type

```http
400 Bad Request
```

```json
{
  "detail": "Unsupported image type. Use JPEG, PNG, or WEBP."
}
```

### Image Too Large

```http
413 Payload Too Large
```

```json
{
  "detail": "Image is too large. Maximum size is 5 MB."
}
```

### Invalid Image

```http
400 Bad Request
```

```json
{
  "detail": "Invalid or corrupted image."
}
```

### Model Missing

```http
503 Service Unavailable
```

```json
{
  "detail": "Computer vision model is not available."
}
```

### Inference Failure

```http
500 Internal Server Error
```

```json
{
  "detail": "Model inference failed."
}
```

### Database Failure

```http
503 Service Unavailable
```

```json
{
  "detail": "Prediction could not be stored in the database."
}
```

---

# 3. Prediction History

```http
GET /api/v1/predictions
```

Returns prediction records ordered from newest to oldest.

Example:

```json
[
  {
    "id": 5,
    "image_name": "face.jpg",
    "predicted_class": "happy",
    "confidence": 0.91,
    "top_k_predictions": [],
    "inference_ms": 31.2,
    "model_version": "1.0.0",
    "created_at": "2026-08-15T13:30:00"
  }
]
```

---

# 4. Prediction by ID

```http
GET /api/v1/predictions/{prediction_id}
```

Example:

```http
GET /api/v1/predictions/5
```

If found, a single prediction record is returned.

If not found:

```http
404 Not Found
```

```json
{
  "detail": "Prediction not found"
}
```

---

# 5. Prediction Statistics

```http
GET /api/v1/stats
```

Example:

```json
{
  "total_predictions": 25,
  "class_distribution": {
    "happy": 7,
    "angry": 5,
    "neutral": 6,
    "sad": 3,
    "suprised": 2,
    "tired": 2
  },
  "average_confidence": 0.82
}
```

Statistics are calculated dynamically from PostgreSQL.

---

# 6. Model Information

```http
GET /api/v1/model
```

Example:

```json
{
  "model_name": "MobileNetV3 Small",
  "model_version": "1.0.0",
  "classes": [
    "neutral",
    "angry",
    "happy",
    "sad",
    "suprised",
    "tired"
  ],
  "input_size": [
    224,
    224
  ],
  "deployment_status": "loaded"
}
```

---

# Swagger

FastAPI automatically generates interactive API documentation.

Local:

```text
http://127.0.0.1:8000/docs
```

Production:

```text
<FASTAPI_PRODUCTION_URL>/docs
```
