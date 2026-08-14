# Production Computer Vision Agent

A production-oriented AI system for **facial emotion classification** that combines Computer Vision, FastAPI, PostgreSQL, a React frontend, and an LLM-powered agent.

The system allows users to upload a facial image, classify the detected emotion, view confidence scores and Top-K predictions, store prediction history, analyze statistics, and interact with the system through an AI agent.

---

## Project Overview

This project demonstrates how a Computer Vision model can be transformed from a trained machine learning model into a complete production-style AI application.

The system integrates:

- Computer Vision model training and inference
- FastAPI REST API
- PostgreSQL database
- React + Vite frontend
- LLM-based AI agent
- Tool calling
- Open WebUI integration
- Automated testing
- Docker-based deployment
- Dokploy production deployment

### Supported Emotion Classes

The model currently supports six facial emotion classes:

1. Angry
2. Happy
3. Neutral
4. Sad
5. Suprised
6. Tired

> Note: `suprised` follows the original dataset/model label spelling.

---

## System Architecture

The main application workflow is:

```text
User
  │
  ▼
React Frontend
  │
  ▼
FastAPI Backend
  │
  ├──────────────► Computer Vision Model
  │                     │
  │                     ▼
  │               Emotion Prediction
  │
  ▼
PostgreSQL Database
  │
  ▼
Prediction History & Statistics
```

The AI Agent workflow is:

```text
User
  │
  ▼
Open WebUI
  │
  ▼
LLM / AI Agent
  │
  ▼
Agent Tools
  │
  ▼
FastAPI Backend
  │
  ├──────────────► CV Model
  │
  └──────────────► PostgreSQL
  │
  ▼
Tool Result
  │
  ▼
LLM Response
  │
  ▼
User
```

More architecture information is available in:

```text
docs/architecture.md
```

---

## Dataset

The project uses a facial emotion image-classification dataset from **Roboflow Universe**.

### Task

Multi-class image classification.

### Classes

```text
angry
happy
neutral
sad
suprised
tired
```

### Data Processing

Image preprocessing is performed dynamically during training and inference instead of saving duplicated processed images to disk.

The preprocessing pipeline includes:

- Resize with padding
- 224 × 224 RGB input
- Conversion to tensor
- ImageNet normalization

Training augmentation additionally includes:

- Random horizontal flip
- Color jitter

The dataset exploration notebook is available at:

```text
training/01_dataset_exploration.ipynb
```

---

## Computer Vision Model

### Architecture

The current model uses:

```text
MobileNetV3 Small
```

with transfer learning using PyTorch.

### Input

```text
RGB Image
224 × 224 pixels
```

### Output

The inference pipeline returns:

- Predicted emotion class
- Confidence score
- Top-3 predictions
- Inference latency
- Model version

### Model Artifacts

The production model artifacts are stored in:

```text
models/
├── model.pt
├── labels.json
└── model_metrics.json
```

The inference pipeline loads the model once and reuses it for subsequent prediction requests.

---

## Model Evaluation

The currently stored evaluation report includes:

| Metric | Value |
|---|---:|
| Best Validation Accuracy | 96% |
| Test Accuracy | 96% |
| Number of Classes | 6 |
| Test Set Size | 127 |
| Training Epochs | 10 |

### Per-Class F1 Scores

| Class | F1 Score |
|---|---:|
| Angry | 0.96 |
| Happy | 0.97 |
| Neutral | 0.92 |
| Sad | 0.94 |
| Suprised | 0.97 |
| Tired | 1.00 |

> The current test set is relatively small, so the reported evaluation metrics may have high variance. The model is also being re-validated on external images before final production deployment.

---

## Backend API

The backend is implemented using **FastAPI**.

FastAPI provides:

- REST endpoints
- Request validation
- Error handling
- Automatic Swagger documentation
- Integration with the CV model
- Integration with PostgreSQL

### Local Backend URL

```text
http://127.0.0.1:8000
```

### Swagger Documentation

When the backend is running:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Checks the status of:

- API
- PostgreSQL database
- Computer Vision model

Example:

```json
{
  "api": "healthy",
  "database": "healthy",
  "model": "loaded"
}
```

---

### Predict Emotion

```http
POST /api/v1/predict
```

Input:

```text
multipart/form-data
image=<image file>
```

Supported formats:

```text
JPEG
PNG
WEBP
```

Maximum upload size:

```text
5 MB
```

Example response:

```json
{
  "id": 1,
  "image_name": "face.jpg",
  "predicted_class": "happy",
  "confidence": 0.94,
  "top_k_predictions": [
    {
      "class_name": "happy",
      "probability": 0.94
    },
    {
      "class_name": "neutral",
      "probability": 0.04
    },
    {
      "class_name": "sad",
      "probability": 0.02
    }
  ],
  "inference_ms": 31.4,
  "model_version": "1.0.0",
  "created_at": "2026-08-15T00:00:00"
}
```

---

### Prediction History

```http
GET /api/v1/predictions
```

Returns stored predictions ordered by recent predictions.

---

### Prediction by ID

```http
GET /api/v1/predictions/{prediction_id}
```

Returns a specific prediction stored in PostgreSQL.

---

### Prediction Statistics

```http
GET /api/v1/stats
```

Returns:

- Total number of predictions
- Class distribution
- Average confidence

---

### Model Information

```http
GET /api/v1/model
```

Returns information about the currently deployed CV model.

---

## PostgreSQL Database

Prediction results are persisted in PostgreSQL.

Each prediction stores:

```text
id
image_name
predicted_class
confidence
top_k_predictions
inference_ms
model_version
created_at
```

This enables the application to provide:

- Prediction history
- Prediction lookup
- Class distribution
- Average confidence
- Total prediction statistics

---

## Frontend

The user interface is built using:

```text
React
Vite
JavaScript
CSS
```

### Main Features

The frontend provides:

- Image upload
- Image preview
- Emotion classification
- Predicted class
- Confidence score
- Top-3 prediction probabilities
- Inference time
- Model version
- Prediction ID
- Loading state
- Error handling
- Prediction statistics
- Class distribution
- Prediction history
- Responsive layout

### Frontend Workflow

```text
Upload Image
      ↓
Preview Image
      ↓
Analyze Emotion
      ↓
FastAPI Prediction
      ↓
Prediction Result
      ↓
Statistics Update
      ↓
History Update
```

---

## AI Agent

The project includes an LLM-powered agent capable of interacting with the production backend through tools.

The agent uses an **OpenAI-compatible API client**, allowing it to work with OpenAI or other compatible providers depending on the configured environment variables.

The LLM does not directly access the database or CV model.

Instead:

```text
LLM
 ↓
Tool Call
 ↓
FastAPI
 ↓
CV Model / PostgreSQL
 ↓
Real Result
 ↓
LLM
```

This keeps agent responses grounded in real application data.

---

## Agent Tools

The current agent includes the following tools:

### `classify_image`

Classifies a local JPEG, PNG, or WEBP image using the deployed CV model.

### `get_prediction_history`

Retrieves recent predictions stored in PostgreSQL.

### `get_prediction_by_id`

Retrieves one prediction using its database ID.

### `get_prediction_statistics`

Retrieves total predictions, class distribution, and average confidence.

### `get_model_info`

Retrieves information about the currently deployed CV model.

The agent is designed not to fabricate prediction or database results when a backend tool fails.

---

## Open WebUI

Open WebUI provides the conversational interface for interacting with the AI agent.

Expected workflow:

```text
User
 ↓
Open WebUI
 ↓
AI Agent
 ↓
Tool Selection
 ↓
FastAPI
 ↓
Real Application Data
 ↓
Agent Response
```

**Status:** Integration in progress.

This section will be updated with the final Open WebUI configuration and production URL once integration is completed.

---

## Technology Stack

### Computer Vision

- Python
- PyTorch
- Torchvision
- MobileNetV3
- Pillow
- Scikit-learn

### Backend

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Psycopg

### Database

- PostgreSQL

### Frontend

- React
- Vite
- JavaScript
- CSS

### Agent

- OpenAI-compatible API
- OpenAI Python SDK
- Tool / Function Calling
- HTTPX

### Testing

- Pytest
- HTTPX
- ESLint

### Deployment

- Docker
- Docker Compose
- Dokploy

---

## Project Structure

```text
Production_CV_Agent/
│
├── agent/
│   ├── agent.py
│   ├── prompts.py
│   ├── tools.py
│   └── voice.py
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── health.py
│       │   ├── history.py
│       │   ├── model_info.py
│       │   ├── predictions.py
│       │   └── stats.py
│       │
│       ├── services/
│       ├── config.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       └── schemas.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── api.md
│   ├── architecture.md
│   └── demo.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   ├── labels.json
│   ├── model.pt
│   └── model_metrics.json
│
├── openwebui/
│
├── tests/
│   ├── test_agent.py
│   ├── test_health.py
│   └── test_predictions.py
│
├── training/
│   ├── 01_dataset_exploration.ipynb
│   ├── dataset.py
│   ├── evaluate.py
│   ├── inference.py
│   ├── train.py
│   └── transforms.py
│
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Local Installation

## Prerequisites

Install:

- Python 3.11+
- `uv`
- PostgreSQL
- Node.js
- npm

---

## 1. Clone the Repository

```bash
git clone https://github.com/JoudAlrubaish/Production_CV_Agent.git
cd Production_CV_Agent
```

---

## 2. Install Python Dependencies

```bash
uv sync
```

---

## 3. Configure Environment Variables

Copy:

```bash
cp .env.example .env
```

Configure the required variables:

```env
DATABASE_URL=postgresql+psycopg://USER@localhost:5432/cv_agent_db

MODEL_PATH=./models/model.pt
MODEL_VERSION=1.0.0

CORS_ORIGINS=http://localhost:5173

LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

BACKEND_URL=http://localhost:8000
AGENT_REQUEST_TIMEOUT=20
```

Never commit the real `.env` file or API keys to GitHub.

---

## 4. Create PostgreSQL Database

Example:

```bash
createdb cv_agent_db
```

Update `DATABASE_URL` in `.env` based on your PostgreSQL configuration.

---

## 5. Run FastAPI

From the project root:

```bash
uv run uvicorn backend.app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Run the React Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 7. Run the Agent

Make sure:

1. PostgreSQL is running.
2. FastAPI is running.
3. `LLM_API_KEY` is configured.

Then:

```bash
uv run python -m agent.agent
```

Example questions:

```text
What model is currently deployed?

Show me the latest 5 predictions.

What are the prediction statistics?
```

---

# Testing

## Backend and Agent Tests

From the project root:

```bash
uv run python -m pytest -v
```

The automated test suite covers areas including:

- Health endpoint
- Model loading
- Valid prediction request
- Invalid image request
- Database insertion
- Prediction history
- Agent tool behavior
- Agent backend failure handling

---

## Frontend Linting

```bash
cd frontend
npm run lint
```

---

## Frontend Production Build

```bash
npm run build
```

The production frontend build is generated in:

```text
frontend/dist/
```

---

# Environment Variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection |
| `MODEL_PATH` | Location of CV model |
| `MODEL_VERSION` | Current model version |
| `CORS_ORIGINS` | Allowed frontend origins |
| `LLM_API_KEY` | LLM provider API key |
| `LLM_BASE_URL` | OpenAI-compatible API URL |
| `LLM_MODEL` | LLM model |
| `BACKEND_URL` | FastAPI URL used by agent |
| `AGENT_REQUEST_TIMEOUT` | Agent HTTP request timeout |
| `STT_MODEL` | Speech-to-text model |
| `VOICE_LANGUAGE` | Voice language |
| `VOICE_SAMPLE_RATE` | Audio sample rate |
| `VOICE_RECORD_SECONDS` | Voice recording duration |

---

# Docker Deployment

Docker deployment will package the production components into reproducible containers.

The final Docker Compose configuration is expected to include:

```text
Backend
Frontend
PostgreSQL
Open WebUI
```

**Status:** In progress.

This section will be updated after Docker integration is completed.

---

# Dokploy Deployment

The final system will be deployed using **Dokploy**.

The final production deployment will provide public access to:

- React frontend
- FastAPI / Swagger API
- Open WebUI

**Status:** Not deployed yet.

### Production URLs

```text
Frontend:   TODO
FastAPI:    TODO
Swagger:    TODO
Open WebUI: TODO
```

---

# Security Considerations

The application includes several production-oriented security controls:

- Environment variables are stored outside source code.
- `.env` is excluded from Git.
- Image formats are validated.
- Upload size is restricted.
- Uploaded filenames are sanitized.
- CORS is configurable.
- Database access goes through the backend.
- Agent tools use real backend endpoints.
- The LLM is not allowed to fabricate backend results.

Additional production security configuration will be applied during deployment.

---

# Known Limitations

- The current dataset test split is relatively small.
- Evaluation results may therefore have high variance.
- Generalization to facial images outside the training dataset requires further validation.
- Open WebUI integration is still being finalized.
- Docker and Dokploy deployment are not yet completed.
- Emotion classification predictions should not be interpreted as psychological or medical assessments.

---

# Future Improvements

Potential improvements include:

- Expand the training dataset.
- Improve model generalization.
- Compare multiple transfer-learning architectures.
- Improve augmentation and class balancing.
- Add model monitoring.
- Add prediction confidence thresholds.
- Add authentication and authorization.
- Add CI/CD pipelines.
- Add more advanced dashboard visualizations.
- Add production logging and monitoring.
- Improve agent capabilities.
- Complete voice interaction support.

---

# Team Contributions

| Team Member | Main Responsibility |
|---|---|
| Lama Alghailan | Dataset preparation, CV model training, evaluation, inference |
| Joud Alrubaish | FastAPI backend, PostgreSQL, API endpoints, backend testing |
| Lama Alfreah | AI agent, tools, LLM integration, Open WebUI |
| Fay Almasoud | React frontend, integration, Docker, Dokploy deployment |


---

# Project Status

Current development status:

```text
Computer Vision Model       Under re-validation
FastAPI Backend             Complete
PostgreSQL                  Complete
Automated Tests             Complete
React Frontend              Complete
AI Agent Core               Complete
Open WebUI                  In Progress
Docker                      Pending
Docker Compose              Pending
Dokploy Deployment          Pending
Final Production Testing    Pending
```

---

# Documentation

Additional documentation:

```text
docs/api.md
docs/architecture.md
docs/demo.md
models/model_metrics.json
```

---

## Disclaimer

This project was developed for educational purposes as a production-style Computer Vision and Agentic AI system.

Facial emotion classification is probabilistic and should not be used to make medical, psychological, employment, legal, or other high-impact decisions.
