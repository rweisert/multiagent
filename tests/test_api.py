"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self, client):
        """Test basic health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "multi-agent-api"

    def test_readiness_check(self, client):
        """Test readiness check."""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"


class TestAgentEndpoints:
    """Tests for agent endpoints."""

    def test_list_agents(self, client):
        """Test listing available agents."""
        response = client.get("/api/v1/agents/")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 3

        agent_names = [a["name"] for a in data["agents"]]
        assert "researcher" in agent_names
        assert "writer" in agent_names
        assert "reviewer" in agent_names


class TestWorkflowEndpoints:
    """Tests for workflow endpoints."""

    def test_list_workflows(self, client):
        """Test listing available workflows."""
        response = client.get("/api/v1/workflows/")
        assert response.status_code == 200
        data = response.json()
        assert "workflows" in data
        assert len(data["workflows"]) == 2

        workflow_names = [w["name"] for w in data["workflows"]]
        assert "content-pipeline" in workflow_names
        assert "research" in workflow_names
