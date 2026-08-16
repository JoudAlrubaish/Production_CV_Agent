# Production Computer Vision Agent — EmotionAI

EmotionAI is a production-oriented Computer Vision and Agentic AI system for **facial emotion classification**.

The project transforms a trained deep-learning model into a complete AI application by integrating:

- PyTorch Computer Vision inference
- FastAPI REST services
- PostgreSQL persistence
- React + Vite frontend
- LLM-powered agent
- Open WebUI
- Tool / function calling
- Automated testing
- Docker and Docker Compose
- Dokploy production deployment

The system allows users to upload facial images, classify the visible facial expression, inspect confidence scores and Top-K predictions, review prediction history and statistics, and interact with the backend using a grounded AI assistant.

---

## 1. Problem Statement

A trained Computer Vision model alone is not a complete production system.

Real-world AI applications also require:

- A reusable inference pipeline
- An API layer
- Persistent data storage
- A user interface
- Monitoring and health checks
- Automated testing
- Agentic interaction
- Containerization
- Deployment

EmotionAI was developed to demonstrate this full lifecycle.

The system classifies facial images into one of six expression classes and exposes the model through both a traditional web application and an LLM-powered conversational interface.

---

## 2. Objectives

The main objectives of the project are to:

1. Train and evaluate a multi-class facial emotion classifier.
2. Save the trained model as a reusable production artifact.
3. Serve model inference through FastAPI.
4. Store predictions in PostgreSQL.
5. Build APIs for prediction history, statistics, health, and model information.
6. Build a responsive React frontend.
7. Create an LLM-powered agent using real backend tools.
8. Integrate the agent with Open WebUI.
9. Validate the system using automated tests.
10. Package the application with Docker.
11. Deploy the full system using Dokploy.

---

## 3. Supported Emotion Classes

The current model supports six classes:

```text
angry
happy
neutral
sad
suprised
tired
```

> `suprised` intentionally follows the label spelling used by the original dataset and trained model.

---

## 4. High-Level Architecture

### Main Computer Vision Application

```text
User
  │
  ▼
React Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
Image Validation
  │
  ▼
MobileNetV3 Inference
  │
  ▼
Prediction Result
  │
  ▼
PostgreSQL
  │
  ├────────► Prediction History
  └────────► Statistics Dashboard
```

### Agentic AI Workflow

```text
User
  │
  ▼
Open WebUI
  │
  ▼
LLM
  │
  ▼
Agent Tool Selection
  │
  ▼
FastAPI Backend
  │
  ├────────► CV Model
  └────────► PostgreSQL
  │
  ▼
Grounded Tool Result
  │
  ▼
LLM Response
  │
  ▼
User
```

More details are available in:

```text
docs/architecture.md
```

---

# 5. Dataset

The project uses a facial-emotion image-classification dataset from **Roboflow Universe**.

Dataset URL:

```text
<ROBOFLOW_DATASET_URL>
```

The data is organized into:

```text
train/
valid/
test/
```

with six class folders.

Example:

```text
data/raw/
├── train/
│   ├── angry/
│   ├── happy/
│   ├── neutral/
│   ├── sad/
│   ├── suprised/
│   └── tired/
│
├── valid/
└── test/
```

Raw data is excluded from Git because datasets can be large and should not normally be versioned directly in the repository.

---

# 6. Image Preprocessing

Images are processed dynamically during training and inference.

The evaluation preprocessing pipeline includes:

- RGB conversion
- Resize with padding
- Final input size of 224 × 224
- Conversion to tensor
- ImageNet normalization

Training additionally uses:

- Random horizontal flipping
- Color jitter

The implementation is available in:

```text
training/transforms.py
```

---

# 7. Computer Vision Model

The production classifier is based on:

```text
MobileNetV3 Small
```

using PyTorch and transfer learning.

The original ImageNet pretrained architecture is modified so that the final classification layer outputs six classes.

### Model Input

```text
RGB image
224 × 224
```

### Model Output

The inference service produces:

- Predicted class
- Confidence
- Top-3 predictions
- Inference latency
- Model version

### Model Artifacts

```text
models/
├── model.pt
├── labels.json
└── model_metrics.json
```

The model is loaded once by the production inference layer and reused across requests.

---

# 8. Model Evaluation

The stored evaluation report contains:

| Metric | Result |
|---|---:|
| Best Validation Accuracy | 96% |
| Final Test Accuracy | 96% |
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

The test set is relatively small, so the metrics should be interpreted with that limitation in mind.

Additional validation during integration also showed that model performance can decrease on some external real-world images that differ from the original dataset distribution.

See:

```text
docs/model.md
docs/limitations.md
```

---

# 9. Backend

The backend is implemented using **FastAPI**.

It provides:

- Model inference
- Input validation
- PostgreSQL integration
- Prediction persistence
- History endpoints
- Statistics
- Model metadata
- Health checks
- Swagger/OpenAPI documentation
- Error handling

Local API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 10. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API, database, and model health |
| POST | `/api/v1/predict` | Classify an uploaded image |
| GET | `/api/v1/predictions` | Retrieve prediction history |
| GET | `/api/v1/predictions/{id}` | Retrieve one prediction |
| GET | `/api/v1/stats` | Retrieve prediction statistics |
| GET | `/api/v1/model` | Retrieve deployed model information |

Full documentation:

```text
docs/api.md
```

---

# 11. Image Upload Validation

The prediction endpoint accepts:

```text
JPEG
PNG
WEBP
```

Maximum file size:

```text
5 MB
```

The backend validates:

- MIME type
- File size
- Actual image validity
- Model availability
- Database persistence

Unsafe filename paths are removed before storing the image name.

---

# 12. Prediction Response

Example:

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
      "probability": 0.0418
    },
    {
      "class_name": "sad",
      "probability": 0.017
    }
  ],
  "inference_ms": 31.4,
  "model_version": "1.0.0",
  "created_at": "2026-08-15T12:00:00"
}
```

---

# 13. PostgreSQL Database

Predictions are persisted using PostgreSQL and SQLAlchemy.

Each prediction contains:

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

The database supports:

- Prediction history
- Prediction lookup
- Total prediction count
- Class distribution
- Average confidence

---

# 14. Frontend

The frontend is implemented using:

```text
React
Vite
JavaScript
CSS
```

Main features include:

- Image upload
- Image preview
- Analyze button
- Loading state
- Error state
- Prediction class
- Confidence score
- Top-K predictions
- Probability bars
- Inference time
- Model version
- Prediction ID
- Statistics dashboard
- Class distribution
- Recent prediction history
- Responsive layout

Frontend documentation:

```text
docs/frontend.md
```

---

# 15. AI Agent

The project includes an LLM-powered agent that interacts with the application through backend tools.

The LLM does not directly query PostgreSQL or access the CV model.

Instead:

```text
LLM
 ↓
Tool Call
 ↓
FastAPI
 ↓
Model / Database
 ↓
Real Result
 ↓
LLM
```

This approach keeps operational answers grounded in actual system data.

---

# 16. Agent Tools

The system provides five main tools:

### `get_model_info`

Returns information about the deployed Computer Vision model.

### `get_prediction_history`

Returns recent predictions stored in PostgreSQL.

### `get_prediction_by_id`

Returns a specific prediction.

### `get_prediction_statistics`

Returns total predictions, class distribution, and average confidence.

### `classify_image`

Classifies an image that is accessible to the agent/Open WebUI server.

---

# 17. Open WebUI

Open WebUI provides the conversational interface for the agent.

Files:

```text
openwebui/
├── README.md
├── system_prompt.txt
└── tools.py
```

The Open WebUI tools call the real FastAPI backend.

The system prompt explicitly prevents the LLM from inventing:

- Prediction results
- Confidence values
- Prediction IDs
- Statistics
- Model metadata

If the backend is unavailable, the assistant must report the failure instead of generating fake operational information.

See:

```text
docs/agent_openwebui.md
```

---

# 18. Technology Stack

| Layer | Technology |
|---|---|
| Computer Vision | PyTorch, Torchvision, MobileNetV3 |
| Image Processing | Pillow |
| Backend | FastAPI, Uvicorn |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Validation | Pydantic |
| Frontend | React, Vite |
| Agent | OpenAI-compatible LLM / Tool Calling |
| Agent HTTP Client | HTTPX |
| Conversational UI | Open WebUI |
| Testing | Pytest, HTTPX, ESLint |
| Containers | Docker |
| Orchestration | Docker Compose |
| Web Server | Nginx |
| Deployment | Dokploy |

---

# 19. Repository Structure

```text
Production_CV_Agent/
│
├── agent/
│
├── backend/
│   ├── Dockerfile
│   └── app/
│       ├── api/
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
│   ├── model.md
│   ├── frontend.md
│   ├── agent_openwebui.md
│   ├── deployment.md
│   ├── testing.md
│   ├── demo.md
│   ├── limitations.md
│   └── team_contributions.md
│
├── frontend/
│   ├── Dockerfile
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
│   ├── README.md
│   ├── system_prompt.txt
│   └── tools.py
│
├── tests/
│
├── training/
│   ├── 01_dataset_exploration.ipynb
│   ├── dataset.py
│   ├── evaluate.py
│   ├── inference.py
│   ├── train.py
│   └── transforms.py
│
├── compose.yaml
├── .dockerignore
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 20. Local Installation

## Prerequisites

Install:

```text
Python 3.11+
uv
PostgreSQL
Node.js
npm
Docker
```

---

## Clone Repository

```bash
git clone https://github.com/JoudAlrubaish/Production_CV_Agent.git

cd Production_CV_Agent
```

---

## Install Python Dependencies

```bash
uv sync
```

---

## Environment Variables

Create:

```bash
cp .env.example .env
```

Example:

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

Never commit real credentials or API keys.

---

# 21. Run Locally

## PostgreSQL

Create the local database:

```bash
createdb cv_agent_db
```

---

## FastAPI

From project root:

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

## React Frontend

```bash
cd frontend

npm install

npm run dev
```

Default Vite URL:

```text
http://localhost:5173
```

---

# 22. Docker

The backend and frontend each have their own Dockerfile.

The backend container uses Python and `uv`.

The frontend uses a multi-stage build:

```text
Node.js
   ↓
Vite production build
   ↓
Nginx
```

---

# 23. Docker Compose

The project contains:

```text
compose.yaml
```

The stack includes:

```text
postgres
backend
frontend
open-webui
```

Start:

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

Default mapped ports in the current Compose configuration are:

| Service | Port |
|---|---|
| Backend | `8010` |
| Frontend | `3010` |
| Open WebUI | `8080` |

---

# 24. Dokploy Deployment

The project is deployed using Dokploy.

Production URLs:

```text
Frontend:
<FRONTEND_PRODUCTION_URL>

FastAPI:
<FASTAPI_PRODUCTION_URL>

Swagger:
<FASTAPI_PRODUCTION_URL>/docs

Open WebUI:
<OPEN_WEBUI_PRODUCTION_URL>
```

Deployment documentation:

```text
docs/deployment.md
```

---

# 25. Automated Testing

Run backend and agent tests:

```bash
uv run python -m pytest -v
```

The tests cover areas such as:

- API health
- Model loading
- Valid prediction
- Invalid image handling
- Database insertion
- Prediction history
- Agent tools
- Backend failure handling
- Grounding rules

---

# 26. Frontend Validation

```bash
cd frontend

npm run lint

npm run build
```

Production files are generated under:

```text
frontend/dist/
```

---

# 27. Security Considerations

The project includes:

- `.env` excluded from Git
- Configurable environment variables
- File type validation
- Maximum upload size
- Corrupted-image detection
- Filename sanitization
- Configurable CORS
- Backend-controlled database access
- Grounded LLM tool usage

For production environments, database passwords and API keys must be stored using secure environment-variable or secret-management mechanisms.

---

# 28. Known Limitations

The current model performs strongly on the held-out dataset but has reduced generalization on some external images.

Important limitations include:

- Small test set
- Possible dataset/domain shift
- External-image generalization
- Facial-expression ambiguity
- Some class confusion
- Visible facial expression does not necessarily represent a person's internal emotional state

The system should therefore be considered an educational Computer Vision application rather than a psychological assessment system.

More information:

```text
docs/limitations.md
```

---

# 29. Future Improvements

Future development may include:

- More diverse training data
- External validation datasets
- Improved data augmentation
- Class balancing
- Architecture comparison
- Confidence calibration
- Model monitoring
- Authentication
- Authorization
- CI/CD
- Production observability
- Centralized logging
- Improved agent file handling
- Automated model version management

---

# 30. Team Contributions

| Team Member | Responsibility |
|---|---|
| `<STUDENT_1_NAME>` | Dataset, training, evaluation, CV inference |
| `<STUDENT_2_NAME>` | FastAPI, PostgreSQL, APIs, backend testing |
| `<STUDENT_3_NAME>` | Agent, LLM integration, tools, Open WebUI |
| `<STUDENT_4_NAME>` | React frontend, integration, Docker, deployment |

Detailed contributions:

```text
docs/team_contributions.md
```

---

# 31. Final System Workflow

```text
DATA
 ↓
MODEL TRAINING
 ↓
MODEL ARTIFACT
 ↓
INFERENCE
 ↓
FASTAPI
 ↓
POSTGRESQL
 ↓
REACT FRONTEND
 ↓
AGENT TOOLS
 ↓
OPEN WEBUI
 ↓
DOCKER
 ↓
DOKPLOY
 ↓
PRODUCTION
```
