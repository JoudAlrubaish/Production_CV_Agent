"""
title: EmotionAI Production Tools
author: Production CV Agent Team
description: Grounded Open WebUI tools for the EmotionAI FastAPI backend.
required_open_webui_version: 0.4.0
requirements: httpx,pydantic
version: 1.0.0
license: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx
from pydantic import BaseModel, Field


class Tools:
    """Open WebUI workspace tools backed by the real FastAPI service."""

    class Valves(BaseModel):
        backend_url: str = Field(
            default="http://backend:8000",
            description=(
                "FastAPI base URL. Use http://backend:8000 when Open WebUI and "
                "the backend share a Docker Compose network. Use "
                "http://host.docker.internal:8000 when Open WebUI is in Docker "
                "but FastAPI runs directly on the host Mac."
            ),
        )
        request_timeout: float = Field(
            default=20.0,
            ge=1.0,
            le=120.0,
            description="HTTP timeout in seconds.",
        )

    def __init__(self):
        self.valves = self.Valves()

    @property
    def _base_url(self) -> str:
        return self.valves.backend_url.rstrip("/")

    async def _request_json(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Call FastAPI and return grounded JSON, or a readable failure string."""
        try:
            async with httpx.AsyncClient(timeout=self.valves.request_timeout) as client:
                response = await client.request(
                    method,
                    f"{self._base_url}{path}",
                    **kwargs,
                )
        except httpx.RequestError as exc:
            return {
                "ok": False,
                "error": f"Could not reach the FastAPI backend: {exc}",
            }

        if response.is_error:
            try:
                payload = response.json()
                detail = payload.get("detail", payload)
            except Exception:
                detail = response.text or "unknown backend error"
            return {
                "ok": False,
                "status_code": response.status_code,
                "error": str(detail),
            }

        try:
            return {"ok": True, "data": response.json()}
        except ValueError:
            return {
                "ok": False,
                "error": "Backend returned a non-JSON response.",
            }

    async def get_model_info(self) -> dict[str, Any]:
        """
        Get information about the currently deployed facial-emotion model.

        Use this tool whenever the user asks which model is deployed, its version,
        classes, input size, or deployment status. Never guess these values.
        """
        return await self._request_json("GET", "/api/v1/model")

    async def get_prediction_history(self, limit: int = 5) -> dict[str, Any]:
        """
        Get the most recent prediction records from the real PostgreSQL database.

        :param limit: Number of latest predictions to return, from 1 to 100.
        """
        if limit < 1 or limit > 100:
            return {"ok": False, "error": "limit must be between 1 and 100."}

        result = await self._request_json("GET", "/api/v1/predictions")
        if result.get("ok") and isinstance(result.get("data"), list):
            result["data"] = result["data"][:limit]
        return result

    async def get_prediction_by_id(self, prediction_id: int) -> dict[str, Any]:
        """
        Get one stored prediction by its database ID.

        :param prediction_id: Positive PostgreSQL prediction ID.
        """
        if prediction_id < 1:
            return {
                "ok": False,
                "error": "prediction_id must be a positive integer.",
            }
        return await self._request_json(
            "GET",
            f"/api/v1/predictions/{prediction_id}",
        )

    async def get_prediction_statistics(self) -> dict[str, Any]:
        """
        Get real prediction statistics from PostgreSQL.

        Use this tool for total prediction count, class distribution, average
        confidence, or questions such as which class has been predicted most often.
        Never invent statistics when the backend is unavailable.
        """
        return await self._request_json("GET", "/api/v1/stats")

    async def classify_image(self, image_path: str) -> dict[str, Any]:
        """
        Classify a JPEG, PNG, or WEBP image that is accessible to the Open WebUI server.

        :param image_path: Server-side image path accessible to the Open WebUI process.
        """
        path = Path(image_path).expanduser()
        if not path.is_file():
            return {
                "ok": False,
                "error": f"Image file does not exist on the Open WebUI server: {path}",
            }

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        content_type = mime_types.get(path.suffix.lower())
        if content_type is None:
            return {
                "ok": False,
                "error": "Unsupported image type. Use JPEG, PNG, or WEBP.",
            }

        try:
            content = path.read_bytes()
        except OSError as exc:
            return {"ok": False, "error": f"Could not read image: {exc}"}

        return await self._request_json(
            "POST",
            "/api/v1/predict",
            files={"image": (path.name, content, content_type)},
        )
