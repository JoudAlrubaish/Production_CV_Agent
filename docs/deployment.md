# Deployment Documentation

## Overview

EmotionAI uses:

```text
Docker
Docker Compose
Dokploy
```

to package and deploy the application.

---

# Services

The Compose stack contains:

```text
postgres
backend
frontend
open-webui
```

---

# PostgreSQL

Docker image:

```text
postgres:16
```

Internal database:

```text
cvapp
```

The database uses a persistent Docker volume:

```text
postgres_data
```

This keeps predictions after container restarts.

---

# Backend Container

Dockerfile:

```text
backend/Dockerfile
```

Base:

```text
python:3.12-slim
```

Package manager:

```text
uv
```

Startup:

```text
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

---

# Frontend Container

Dockerfile:

```text
frontend/Dockerfile
```

Build stage:

```text
node:20-alpine
```

Production server:

```text
nginx:alpine
```

Workflow:

```text
npm install
 ↓
npm run build
 ↓
Copy dist/
 ↓
Nginx
```

---

# Open WebUI

Image:

```text
ghcr.io/open-webui/open-webui:main
```

Persistent data volume:

```text
open_webui_data
```

---

# Docker Compose

Start:

```bash
docker compose up --build
```

Background:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

Logs:

```bash
docker compose logs
```

Specific service:

```bash
docker compose logs backend
```

Stop:

```bash
docker compose down
```

---

# Local Docker Ports

Current Compose mapping:

```text
Backend     localhost:8010
Frontend    localhost:3010
Open WebUI  localhost:8080
```

PostgreSQL is used internally by the backend.

---

# Docker Networking

Inside the Compose network:

```text
backend → postgres:5432
```

Open WebUI can use:

```text
http://backend:8000
```

to call FastAPI.

---

# Environment Variables

Important variables include:

```env
DATABASE_URL=
MODEL_PATH=
MODEL_VERSION=
CORS_ORIGINS=
LLM_API_KEY=
LLM_BASE_URL=
LLM_MODEL=
BACKEND_URL=
AGENT_REQUEST_TIMEOUT=
```

---

# Production Secrets

Production credentials should not be committed into Git.

Use Dokploy environment variables or secret configuration.

Do not commit:

```text
API keys
Database passwords
Production tokens
Private URLs requiring authentication
```

---

# Dokploy Deployment

The repository is connected to Dokploy.

Deployment components include:

```text
Frontend
FastAPI
PostgreSQL
Open WebUI
```

Production domains:

```text
Frontend:
<FRONTEND_PRODUCTION_URL>

Backend:
<FASTAPI_PRODUCTION_URL>

Swagger:
<FASTAPI_PRODUCTION_URL>/docs

Open WebUI:
<OPEN_WEBUI_PRODUCTION_URL>
```

---

# Deployment Verification

After deployment, verify:

```text
Frontend loads
Backend /health is healthy
Swagger opens
Prediction request works
Prediction is stored
History returns data
Statistics return data
Open WebUI loads
Open WebUI tool can reach FastAPI
Grounded agent response works
```

---

# Health Check

Production test:

```bash
curl <FASTAPI_PRODUCTION_URL>/health
```

Expected:

```json
{
  "api": "healthy",
  "database": "healthy",
  "model": "loaded"
}
```

---

# Model Volume

The backend expects the model to be available at the configured:

```text
MODEL_PATH
```

In Docker, the model directory can be mounted into the backend container.

---

# Persistent Volumes

The stack uses persistent volumes for:

```text
PostgreSQL
Open WebUI
```

This prevents state loss when containers restart.

---

# Production CORS

`CORS_ORIGINS` should contain only valid frontend domains.

Example:

```text
https://emotionai.example.com
```

Avoid using unrestricted CORS in production unless required.

---

# Troubleshooting

## Backend Cannot Reach PostgreSQL

Check:

```text
DATABASE_URL
postgres service status
Docker network
PostgreSQL logs
```

---

## Model Not Loaded

Check:

```text
MODEL_PATH
models/model.pt
mounted volume
file permissions
```

---

## Open WebUI Cannot Reach Backend

When both run in Compose, use:

```text
http://backend:8000
```

not:

```text
localhost
```

because `localhost` inside the Open WebUI container refers to that container itself.

---

## Frontend Cannot Reach Backend

Confirm that the frontend API base URL points to the deployed FastAPI address or reverse proxy.

---

# Final Deployment Checklist

```text
[ ] Containers running
[ ] Database persistent
[ ] Model available
[ ] Health endpoint healthy
[ ] Frontend accessible
[ ] Swagger accessible
[ ] Prediction works
[ ] Database insertion works
[ ] Statistics work
[ ] Open WebUI accessible
[ ] Agent tools work
[ ] Secrets protected
```
