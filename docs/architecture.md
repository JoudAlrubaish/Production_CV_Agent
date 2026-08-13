# System Architecture

## Project

Face Emotion Classification Agent

## Dataset

Source: Roboflow Universe

Task: Image Classification

Classes:
- neutral
- angry
- happy
- sad
- suprised
- tired

## Computer Vision Model

Framework: PyTorch

Model: MobileNetV3 Small

Input:
- RGB image
- 224 x 224 pixels

Output:
- Predicted class
- Confidence score
- Top-3 predictions
- Inference latency
- Model version

## Main Application Workflow

User
→ React Frontend
→ FastAPI
→ MobileNetV3
→ Prediction
→ PostgreSQL
→ FastAPI
→ Frontend

## Agent Workflow

User
→ Open WebUI
→ LLM
→ Agent Tool
→ FastAPI
→ PostgreSQL / Model
→ Tool Result
→ LLM
→ User