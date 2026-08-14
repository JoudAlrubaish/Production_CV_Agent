from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
REQUEST_TIMEOUT = float(os.getenv("AGENT_REQUEST_TIMEOUT", "20"))


class ToolError(RuntimeError):
    """Raised when a real application tool cannot complete its request."""


def _json_or_error(response: httpx.Response) -> Any:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = None
        try:
            detail = response.json().get("detail")
        except Exception:
            detail = response.text
        raise ToolError(
            f"Backend returned HTTP {response.status_code}: {detail or 'unknown error'}"
        ) from exc

    try:
        return response.json()
    except ValueError as exc:
        raise ToolError("Backend returned a non-JSON response.") from exc


def classify_image(image_path: str) -> dict[str, Any]:
    """Classify a local JPEG/PNG/WEBP image using the deployed FastAPI model."""
    path = Path(image_path).expanduser()
    if not path.is_file():
        raise ToolError(f"Image file does not exist: {path}")

    mime_by_suffix = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    content_type = mime_by_suffix.get(path.suffix.lower())
    if content_type is None:
        raise ToolError("Unsupported image type. Use JPEG, PNG, or WEBP.")

    try:
        with path.open("rb") as image_file:
            response = httpx.post(
                f"{BACKEND_URL}/api/v1/predict",
                files={"image": (path.name, image_file, content_type)},
                timeout=REQUEST_TIMEOUT,
            )
    except httpx.RequestError as exc:
        raise ToolError(f"Could not reach FastAPI backend: {exc}") from exc

    return _json_or_error(response)


def get_prediction_history(limit: int = 5) -> list[dict[str, Any]]:
    """Return the most recent N stored predictions from PostgreSQL through FastAPI."""
    if limit < 1 or limit > 100:
        raise ToolError("limit must be between 1 and 100.")

    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/v1/predictions",
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.RequestError as exc:
        raise ToolError(f"Could not reach FastAPI backend: {exc}") from exc

    data = _json_or_error(response)
    if not isinstance(data, list):
        raise ToolError("Prediction history response was not a list.")

    # Student 2's current endpoint returns all rows ordered newest first.
    # Slice here so the agent still supports "latest N" without changing backend code.
    return data[:limit]


def get_prediction_by_id(prediction_id: int) -> dict[str, Any]:
    """Return one stored prediction by its database ID."""
    if prediction_id < 1:
        raise ToolError("prediction_id must be a positive integer.")

    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/v1/predictions/{prediction_id}",
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.RequestError as exc:
        raise ToolError(f"Could not reach FastAPI backend: {exc}") from exc

    return _json_or_error(response)


def get_prediction_statistics() -> dict[str, Any]:
    """Return prediction counts, class distribution, and average confidence."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/v1/stats",
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.RequestError as exc:
        raise ToolError(f"Could not reach FastAPI backend: {exc}") from exc

    return _json_or_error(response)


def get_model_info() -> dict[str, Any]:
    """Return information about the currently deployed CV model."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/v1/model",
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.RequestError as exc:
        raise ToolError(f"Could not reach FastAPI backend: {exc}") from exc

    return _json_or_error(response)


TOOL_FUNCTIONS = {
    "classify_image": classify_image,
    "get_prediction_history": get_prediction_history,
    "get_prediction_by_id": get_prediction_by_id,
    "get_prediction_statistics": get_prediction_statistics,
    "get_model_info": get_model_info,
}

# OpenAI-compatible function/tool schemas.
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "classify_image",
            "description": "Classify a local image using the deployed facial-emotion CV model.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Local path to a JPEG, PNG, or WEBP image accessible to the agent process.",
                    }
                },
                "required": ["image_path"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prediction_history",
            "description": "Get the most recent N predictions stored by the deployed system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 5,
                    }
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prediction_by_id",
            "description": "Get one stored prediction by prediction ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prediction_id": {"type": "integer", "minimum": 1}
                },
                "required": ["prediction_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prediction_statistics",
            "description": "Get total predictions, class distribution, and average confidence from the real database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_model_info",
            "description": "Get the deployed model name, version, classes, input size, and deployment status.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]


def execute_tool_call(name: str, arguments: dict[str, Any] | None = None) -> Any:
    """Safely execute one approved tool by name."""
    if name not in TOOL_FUNCTIONS:
        raise ToolError(f"Unknown tool: {name}")
    return TOOL_FUNCTIONS[name](**(arguments or {}))


def execute_tool_call_json(name: str, arguments_json: str | None = None) -> str:
    """Execute a tool from an LLM tool call and serialize its result for the model."""
    try:
        arguments = json.loads(arguments_json or "{}")
    except json.JSONDecodeError as exc:
        raise ToolError("Tool arguments were not valid JSON.") from exc

    result = execute_tool_call(name, arguments)
    return json.dumps(result, ensure_ascii=False, default=str)