# System Architecture

## Overview

EmotionAI is structured as a modular production-oriented AI system.

The architecture separates:

- Computer Vision
- Backend services
- Data persistence
- Frontend
- Agentic AI
- Deployment

This separation allows individual components to be updated without redesigning the complete application.

---

## Main Components

### Computer Vision Layer

Responsible for:

- Model architecture
- Image preprocessing
- Model loading
- Inference
- Confidence calculation
- Top-K prediction generation

Model:

```text
MobileNetV3 Small
```

Framework:

```text
PyTorch
```

---

## Backend Layer

FastAPI acts as the central application layer.

Responsibilities:

```text
Receive request
      ↓
Validate image
      ↓
Run model inference
      ↓
Store prediction
      ↓
Return structured response
```

FastAPI also exposes:

```text
Health
Prediction
History
Statistics
Model information
```

---

## Database Layer

PostgreSQL provides persistent prediction storage.

```text
Prediction
├── id
├── image_name
├── predicted_class
├── confidence
├── top_k_predictions
├── inference_ms
├── model_version
└── created_at
```

SQLAlchemy acts as the ORM layer.

---

## Frontend Layer

The React frontend communicates with FastAPI using HTTP requests.

Prediction flow:

```text
User selects image
        ↓
Browser image preview
        ↓
POST /api/v1/predict
        ↓
FastAPI
        ↓
Model
        ↓
PostgreSQL
        ↓
JSON response
        ↓
React result card
```

After a prediction, React refreshes:

```text
GET /api/v1/stats

GET /api/v1/predictions
```

This updates the dashboard automatically.

---

# Agentic AI Architecture

The agent does not access PostgreSQL directly.

It uses FastAPI as the authoritative application layer.

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
FastAPI
 ↓
Database / Model
 ↓
Tool Result
 ↓
LLM
 ↓
User
```

This improves grounding because operational information comes from real application services.

---

# Open WebUI Architecture

Open WebUI provides the conversational user interface.

```text
Open WebUI
    │
    ▼
Configured LLM
    │
    ▼
EmotionAI Production Tools
    │
    ▼
FastAPI
    │
    ├── /api/v1/model
    ├── /api/v1/predictions
    ├── /api/v1/stats
    └── /api/v1/predict
```

---

# Grounding Strategy

The system prompt requires the LLM to use tools for operational information.

The agent must never fabricate:

```text
Prediction classes
Confidence values
Prediction IDs
Prediction history
Statistics
Model deployment information
```

If FastAPI is unavailable, tool failure is returned to the LLM.

The LLM must report the failure rather than generating an unsupported result.

---

# Container Architecture

The Docker Compose environment contains four main services:

```text
                     Docker Network
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
 PostgreSQL             FastAPI             Open WebUI
      ▲                    ▲
      │                    │
      └──────────────┐     │
                     │     │
                     ▼     │
                React / Nginx
```

Services:

```text
postgres
backend
frontend
open-webui
```

---

# Docker Networking

Inside Docker Compose, services communicate using service names.

Examples:

```text
postgres:5432
backend:8000
```

Open WebUI can therefore reach FastAPI using:

```text
http://backend:8000
```

---

# Production Architecture

The application is deployed through Dokploy.

Conceptually:

```text
Internet
   │
   ├────► Frontend Domain
   │          │
   │          ▼
   │       React/Nginx
   │
   ├────► API Domain
   │          │
   │          ▼
   │       FastAPI
   │          │
   │          ├── Model
   │          └── PostgreSQL
   │
   └────► Open WebUI Domain
              │
              ▼
             LLM
              │
              ▼
          Backend Tools
```

---

# Design Decisions

## FastAPI as a Central Interface

The frontend and the AI agent both rely on FastAPI.

This avoids duplicating application logic.

---

## Persistent Predictions

Predictions are stored in PostgreSQL so that results remain available after the request finishes.

This enables:

```text
History
Statistics
Analytics
Agent queries
```

---

## Separate UI and Agent Interfaces

The React frontend focuses on Computer Vision interaction.

Open WebUI focuses on conversational interaction and operational questions.

Both use the same backend.

---

# Architecture Benefits

The architecture provides:

- Modularity
- Reusability
- Clear separation of responsibilities
- Persistent state
- Tool grounding
- Container portability
- Deployment readiness
