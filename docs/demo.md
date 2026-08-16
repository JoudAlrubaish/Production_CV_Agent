# Final Demo Guide

## Objective

The demo should show that EmotionAI is not only a trained Computer Vision model but a complete production AI system.

Recommended duration:

```text
5–8 minutes
```

---

# Demo 1 — System Introduction

Explain:

> EmotionAI is a production facial-expression classification system combining Computer Vision, FastAPI, PostgreSQL, React, Agentic AI, Open WebUI, Docker, and Dokploy.

Show the high-level architecture.

---

# Demo 2 — Frontend

Open:

```text
<FRONTEND_PRODUCTION_URL>
```

Show:

```text
Image Upload
Image Preview
Prediction Statistics
Recent Predictions
```

---

# Demo 3 — Image Classification

Upload a clear facial image.

Click:

```text
Analyze Emotion
```

Explain the output:

```text
Predicted Class
Confidence
Top-3 Predictions
Inference Time
Model Version
Prediction ID
```

---

# Demo 4 — Database Integration

After classification, scroll to:

```text
Prediction Statistics
```

Show that:

```text
Total Predictions
Average Confidence
Class Distribution
```

have updated.

Then show:

```text
Recent Predictions
```

Explain that the new record is stored in PostgreSQL.

---

# Demo 5 — Swagger

Open:

```text
<FASTAPI_PRODUCTION_URL>/docs
```

Show:

```text
GET /health
POST /api/v1/predict
GET /api/v1/predictions
GET /api/v1/predictions/{id}
GET /api/v1/stats
GET /api/v1/model
```

---

# Demo 6 — Health Endpoint

Run:

```text
GET /health
```

Expected:

```json
{
  "api": "healthy",
  "database": "healthy",
  "model": "loaded"
}
```

Explain that this verifies all three important backend components.

---

# Demo 7 — Open WebUI

Open:

```text
<OPEN_WEBUI_PRODUCTION_URL>
```

Ask:

```text
What model is currently deployed?
```

Explain:

```text
LLM
 ↓
get_model_info
 ↓
FastAPI
 ↓
Real model information
```

---

# Demo 8 — Prediction History Through Agent

Ask:

```text
Show me the latest five predictions.
```

Explain that the LLM does not know these records by itself.

It must call:

```text
get_prediction_history
```

which retrieves real PostgreSQL data.

---

# Demo 9 — Statistics Through Agent

Ask:

```text
What is the average prediction confidence?
```

or:

```text
Which class has been predicted most often?
```

Show that the response is generated from:

```text
GET /api/v1/stats
```

---

# Demo 10 — Grounding Explanation

Explain that the system prompt prevents hallucination of operational values.

If the backend fails:

```text
Tool fails
 ↓
Assistant reports failure
```

instead of inventing:

```text
Prediction
Statistics
Confidence
```

---

# Demo 11 — Docker

Show:

```text
compose.yaml
```

Explain that the system contains:

```text
PostgreSQL
FastAPI
React/Nginx
Open WebUI
```

---

# Demo 12 — Dokploy

Show the deployed applications.

Explain that deployment demonstrates that the system works outside the development environment.

---

# Demo 13 — Model Metrics

Show:

```text
models/model_metrics.json
```

Mention:

```text
Validation Accuracy = 96%
Test Accuracy = 96%
```

Also acknowledge that the test set is small.

---

# Demo 14 — Limitations

State clearly:

> The model performs strongly on held-out dataset samples but may show weaker generalization on some external real-world images due to domain shift.

This demonstrates proper model evaluation rather than hiding weaknesses.

---

# Demo 15 — Conclusion

Conclude:

> The project demonstrates the complete lifecycle from dataset and model training to inference, API integration, persistence, frontend interaction, Agentic AI, containerization, and production deployment.
