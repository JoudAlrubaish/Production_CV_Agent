# Agent and Open WebUI Documentation

## Overview

EmotionAI includes an Agentic AI layer that enables conversational interaction with the production system.

The agent is designed around one core principle:

> Operational answers must come from real backend tools rather than from LLM memory or guessing.

---

# Agent Architecture

```text
User Question
    ↓
LLM
    ↓
Tool Decision
    ↓
EmotionAI Tool
    ↓
FastAPI
    ↓
Model / PostgreSQL
    ↓
Tool Result
    ↓
LLM
    ↓
Grounded Answer
```

---

# Agent Core

The Python agent supports OpenAI-compatible LLM APIs.

Configuration:

```env
LLM_API_KEY=
LLM_BASE_URL=
LLM_MODEL=
```

The client sends:

```text
System Prompt
User Message
Tool Schemas
```

to the configured LLM.

When a tool call is requested, the agent executes it and returns the real result to the model.

---

# Open WebUI

Open WebUI provides the final conversational interface.

Files:

```text
openwebui/
├── README.md
├── system_prompt.txt
└── tools.py
```

---

# Open WebUI Tools

## 1. get_model_info

Backend:

```text
GET /api/v1/model
```

Used for questions such as:

```text
What model is deployed?

What is the model version?

What classes are supported?

What is the input size?
```

---

## 2. get_prediction_history

Backend:

```text
GET /api/v1/predictions
```

Used for:

```text
Show the latest predictions.

Show the last five predictions.
```

---

## 3. get_prediction_by_id

Backend:

```text
GET /api/v1/predictions/{id}
```

Used for:

```text
Show prediction ID 5.
```

---

## 4. get_prediction_statistics

Backend:

```text
GET /api/v1/stats
```

Used for:

```text
What is the average confidence?

How many predictions have been made?

Which class appears most often?
```

---

## 5. classify_image

Backend:

```text
POST /api/v1/predict
```

This tool requires a server-accessible image path.

Supported types:

```text
JPEG
PNG
WEBP
```

---

# Tool Grounding

Each Open WebUI tool returns:

```json
{
  "ok": true,
  "data": {}
}
```

or on failure:

```json
{
  "ok": false,
  "error": "..."
}
```

This gives the LLM an explicit signal about whether the operation succeeded.

---

# System Prompt Rules

The system prompt requires the assistant to:

```text
Never fabricate prediction results
Never fabricate confidence values
Never fabricate statistics
Never fabricate prediction IDs
Never fabricate model information
Use tools for operational questions
Report backend failures clearly
```

---

# Backend URL Configuration

When Open WebUI and FastAPI run in the same Compose environment:

```text
http://backend:8000
```

When Open WebUI is inside Docker but FastAPI runs on the Mac host:

```text
http://host.docker.internal:8000
```

When both are running directly on the host:

```text
http://127.0.0.1:8000
```

---

# Open WebUI Setup

1. Open Open WebUI.
2. Go to:

```text
Workspace → Tools
```

3. Create a new tool.
4. Paste:

```text
openwebui/tools.py
```

5. Set `backend_url`.
6. Go to:

```text
Workspace → Models
```

7. Configure the model.
8. Add:

```text
openwebui/system_prompt.txt
```

9. Attach:

```text
EmotionAI Production Tools
```

10. Use native function calling.

---

# Recommended Demo Questions

```text
What model is currently deployed?

Show me the latest five predictions.

What is the average prediction confidence?

Which class has been predicted most often?

Show prediction ID 1.
```

---

# Grounding Failure Test

A useful validation procedure is:

```text
Ask for statistics while backend is running
               ↓
Receive real answer
               ↓
Stop backend
               ↓
Ask same question
               ↓
Tool reports failure
               ↓
Assistant does not invent statistics
```

This demonstrates that the agent is truly grounded in backend data.

---

# Why FastAPI Is Used as the Tool Layer

The agent does not connect directly to PostgreSQL.

Advantages:

```text
Single source of business logic
Consistent validation
Better security
Reusable endpoints
Easier testing
Clear architecture
```
