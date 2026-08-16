# Testing Documentation

## Overview

EmotionAI uses multiple testing layers:

```text
Model Evaluation
Backend Tests
Database Tests
Agent Tests
Frontend Validation
Integration Testing
End-to-End Testing
Deployment Smoke Testing
```

---

# Automated Python Tests

Run:

```bash
uv run python -m pytest -v
```

Tests are located under:

```text
tests/
```

---

# Health Test

Validates:

```text
GET /health
```

and confirms that the API can report:

```text
API status
Database status
Model status
```

---

# Model Loading Test

Confirms that the model artifact is available and can be loaded.

---

# Valid Prediction Test

Tests:

```text
Valid image
 ↓
POST /api/v1/predict
 ↓
Valid response
```

Important fields:

```text
predicted_class
confidence
top_k_predictions
inference_ms
model_version
```

---

# Invalid Prediction Test

Tests rejection of unsupported files and invalid images.

---

# Database Test

Confirms that a prediction can be inserted into PostgreSQL.

---

# Prediction History Test

Validates:

```text
GET /api/v1/predictions
```

---

# Agent Tests

Agent tests validate:

```text
Tool execution
System grounding
Real backend usage
Prediction history
Statistics
Prediction ID lookup
Backend failure handling
```

One important requirement is that the agent must not replace missing backend information with invented data.

---

# Frontend Lint

```bash
cd frontend

npm run lint
```

This verifies JavaScript/React code quality.

---

# Frontend Build

```bash
npm run build
```

This ensures Vite can produce a valid production bundle.

---

# Manual CV Validation

The model should be tested across multiple emotion classes.

Recommended:

```text
Angry
Happy
Neutral
Sad
Suprised
Tired
```

Testing should include:

```text
Dataset-like images
External real-world images
```

because external validation helps identify domain-shift limitations.

---

# API Manual Tests

Swagger:

```text
http://127.0.0.1:8000/docs
```

Recommended endpoints:

```text
/health
/api/v1/model
/api/v1/predict
/api/v1/predictions
/api/v1/predictions/{id}
/api/v1/stats
```

---

# Frontend Integration Test

```text
Upload Image
      ↓
Preview
      ↓
Analyze
      ↓
Prediction
      ↓
Database insert
      ↓
Statistics refresh
      ↓
History refresh
```

All stages should succeed without manual database updates.

---

# Agent Integration Test

Ask Open WebUI:

```text
What model is currently deployed?
```

Expected:

```text
LLM calls get_model_info
 ↓
FastAPI /model
 ↓
Grounded answer
```

---

# Agent Failure Test

Stop FastAPI.

Then ask:

```text
What is the average confidence?
```

Expected behavior:

```text
Tool failure
 ↓
Assistant explains failure
```

Unacceptable:

```text
Assistant invents a value
```

---

# Docker Test

Run:

```bash
docker compose up --build
```

Then verify:

```text
Backend
Frontend
PostgreSQL
Open WebUI
```

---

# Production Smoke Test

After Dokploy deployment verify:

```text
Production frontend loads
Health is healthy
Prediction works
Database persists result
Statistics update
History updates
Open WebUI loads
Tool calls work
```

---

# Acceptance Criteria

The system is considered operational when:

```text
Model loads
API responds
Database stores predictions
Frontend displays results
History works
Statistics work
Agent tools use real backend
Open WebUI works
Docker stack starts
Production deployment is accessible
```
