# Frontend Documentation

## Overview

EmotionAI includes a dedicated web interface built using:

```text
React
Vite
JavaScript
CSS
```

The frontend allows non-technical users to interact with the Computer Vision backend.

---

# Main Features

The interface provides:

```text
Image upload
Image preview
Prediction request
Predicted class
Confidence score
Top-K predictions
Inference time
Model version
Prediction ID
Statistics
Class distribution
Recent history
Loading states
Error states
Responsive layout
```

---

# User Workflow

```text
Open Application
      ↓
Choose Image
      ↓
Preview
      ↓
Analyze Emotion
      ↓
POST /api/v1/predict
      ↓
Receive Prediction
      ↓
Display Result
      ↓
Refresh Statistics
      ↓
Refresh History
```

---

# Image Selection

Accepted formats:

```text
JPG
JPEG
PNG
WEBP
```

The browser displays a local preview before sending the image to FastAPI.

---

# Prediction Request

The image is sent using:

```javascript
FormData
```

with:

```text
image=<selected file>
```

to:

```text
POST /api/v1/predict
```

---

# Loading State

While inference is in progress:

```text
Analyze Emotion
```

changes to:

```text
Analyzing...
```

The button is disabled to prevent duplicate prediction requests.

---

# Prediction Display

A successful response shows:

```text
Predicted emotion
Confidence
Top-3 predictions
Inference time
Model version
Prediction ID
```

Top-K predictions are shown using percentage progress bars.

---

# Statistics Dashboard

The frontend calls:

```text
GET /api/v1/stats
```

and displays:

```text
Total Predictions
Average Confidence
Predicted Classes
Class Distribution
```

---

# Prediction History

The frontend calls:

```text
GET /api/v1/predictions
```

The interface displays the five most recent predictions.

Columns:

```text
ID
Image
Emotion
Confidence
Inference Time
Date
```

---

# Automatic Dashboard Refresh

After every successful prediction:

```text
POST /predict
     ↓
Prediction stored
     ↓
GET /stats
     ↓
GET /predictions
     ↓
Dashboard refreshed
```

No manual browser refresh is required.

---

# Error Handling

The interface displays backend error messages when:

```text
Prediction fails
Backend is unavailable
Invalid image is sent
Database operation fails
```

---

# Responsive Design

The layout adapts for smaller screens.

Desktop layout:

```text
Upload | Preview
```

Mobile layout:

```text
Upload
  ↓
Preview
```

Statistics and result panels also stack vertically on smaller devices.

---

# Development

Install dependencies:

```bash
cd frontend

npm install
```

Run:

```bash
npm run dev
```

---

# Code Quality

Run ESLint:

```bash
npm run lint
```

---

# Production Build

```bash
npm run build
```

Generated output:

```text
frontend/dist/
```

---

# Docker

The frontend Docker build uses:

```text
Node.js
 ↓
npm install
 ↓
Vite build
 ↓
Nginx
```

The final container serves static production files through Nginx.

---

# API Configuration

The frontend must point to the correct FastAPI base URL.

For local development this is commonly:

```text
http://127.0.0.1:8000
```

For production, the API base URL must correspond to the deployed FastAPI service or reverse-proxy route.
