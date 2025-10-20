"""
Pytest configuration y fixtures globales.
"""

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_anthropic_response() -> dict[str, str | list[dict[str, str]]]:
    """Mock response de Anthropic API."""
    return {
        "id": "msg_test123",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Dirección emergente: Enfócate en relaciones hoy.",
            }
        ],
        "model": "claude-sonnet-4-20250514",
        "stop_reason": "end_turn",
    }


@pytest.fixture
def mock_obsidian_vault(tmp_path):  # type: ignore[no-untyped-def]
    """Crea un vault temporal de Obsidian para tests."""
    vault_path = tmp_path / "obsidian-test"
    vault_path.mkdir()
    (vault_path / "30-Sesiones").mkdir()
    return vault_path
