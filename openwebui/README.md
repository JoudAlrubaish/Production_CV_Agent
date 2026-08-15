# Open WebUI Integration — Student 3

This folder contains the final Open WebUI integration for the Agentic AI role.

## Files

- `tools.py`: Open WebUI Workspace Tool with five FastAPI-backed tools.
- `system_prompt.txt`: grounded system prompt for the Open WebUI model/preset.

## Backend URL

Choose the URL based on how the services are running:

- Open WebUI + backend in the same Docker Compose network: `http://backend:8000`
- Open WebUI in Docker while FastAPI runs directly on the host Mac: `http://host.docker.internal:8000`
- Open WebUI and FastAPI both running directly on the same host: `http://127.0.0.1:8000`

## Add the Tool in Open WebUI

1. Start FastAPI and make sure `/health` is healthy.
2. Open Open WebUI.
3. Go to **Workspace → Tools → New Tool**.
4. Paste all of `openwebui/tools.py` and save it.
5. Open the Tool settings/Valves and set `backend_url` to the correct URL above.
6. Go to **Workspace → Models** and create/edit the model used for the demo.
7. Paste `openwebui/system_prompt.txt` into the model System Prompt.
8. Attach **EmotionAI Production Tools** to the model.
9. Keep Function Calling in **Native** mode.
10. Save and open a new chat with that model.

## Required Demo Tests

Run at least these two successful tool calls:

- `What model is currently deployed?`
- `Show me the latest five predictions.`

Recommended additional tests:

- `What is the average prediction confidence?`
- `Which class has been predicted most often?`
- `Show prediction ID 1.`

The answer must come from the real FastAPI tool result. If the backend is stopped, the assistant must report failure instead of inventing data.

## Grounding / Failure Test

1. Ask `What is the average prediction confidence?` while the backend is running.
2. Stop FastAPI.
3. Ask the same question again.
4. The tool should return `ok=false` and the assistant should state that the backend operation failed, without inventing a number.

## Note about classify_image

`classify_image` is exposed as a fifth tool, but its `image_path` must be a path that the Open WebUI server/container can access. For the live demo, image classification can continue through the React frontend while the Open WebUI demo focuses on model information, history, and statistics.