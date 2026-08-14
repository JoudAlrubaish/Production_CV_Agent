import json

import httpx
import pytest

from agent.prompts import SYSTEM_PROMPT
from agent import tools


def _response(status_code: int, payload):
    request = httpx.Request("GET", "http://test")
    return httpx.Response(status_code, json=payload, request=request)


def test_system_prompt_forbids_fabrication():
    prompt = SYSTEM_PROMPT.lower()
    assert "never invent" in prompt
    assert "tool" in prompt
    assert "fails" in prompt or "fail" in prompt


def test_get_model_info_uses_real_backend(monkeypatch):
    expected = {
        "model_name": "MobileNetV3 Small",
        "model_version": "1.0.0",
        "classes": ["happy", "sad"],
        "input_size": [224, 224],
        "deployment_status": "loaded",
    }

    def fake_get(url, timeout):
        assert url.endswith("/api/v1/model")
        return _response(200, expected)

    monkeypatch.setattr(tools.httpx, "get", fake_get)
    assert tools.get_model_info() == expected


def test_prediction_history_respects_limit(monkeypatch):
    rows = [
        {"id": 3, "predicted_class": "happy"},
        {"id": 2, "predicted_class": "neutral"},
        {"id": 1, "predicted_class": "sad"},
    ]

    def fake_get(url, timeout):
        assert url.endswith("/api/v1/predictions")
        return _response(200, rows)

    monkeypatch.setattr(tools.httpx, "get", fake_get)
    assert tools.get_prediction_history(limit=2) == rows[:2]


def test_statistics_tool(monkeypatch):
    expected = {
        "total_predictions": 7,
        "class_distribution": {"happy": 5, "sad": 2},
        "average_confidence": 0.88,
    }

    def fake_get(url, timeout):
        assert url.endswith("/api/v1/stats")
        return _response(200, expected)

    monkeypatch.setattr(tools.httpx, "get", fake_get)
    assert tools.get_prediction_statistics() == expected


def test_prediction_by_id(monkeypatch):
    expected = {"id": 8, "predicted_class": "tired", "confidence": 0.91}

    def fake_get(url, timeout):
        assert url.endswith("/api/v1/predictions/8")
        return _response(200, expected)

    monkeypatch.setattr(tools.httpx, "get", fake_get)
    assert tools.get_prediction_by_id(8) == expected


def test_backend_failure_is_not_fabricated(monkeypatch):
    def fake_get(url, timeout):
        return _response(503, {"detail": "database unavailable"})

    monkeypatch.setattr(tools.httpx, "get", fake_get)

    with pytest.raises(tools.ToolError, match="database unavailable"):
        tools.get_prediction_statistics()


def test_execute_tool_call_json(monkeypatch):
    monkeypatch.setitem(
        tools.TOOL_FUNCTIONS,
        "get_model_info",
        lambda: {"model_name": "demo-model"},
    )
    result = tools.execute_tool_call_json("get_model_info", "{}")
    assert json.loads(result)["model_name"] == "demo-model"