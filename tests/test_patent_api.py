"""Tests for patent report API endpoints."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.api.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


class TestPatentReportsAPI:
    """Tests for patent reports API endpoints."""

    def test_generate_reports_endpoint_exists(self, client):
        """Test that the generate endpoint exists."""
        # Without proper mocking, this will fail, but we can check the route exists
        response = client.post(
            "/api/v1/patent-reports/generate",
            json={
                "patent_pdf_url": "https://example.com/patent.pdf",
                "history_pdf_url": "https://example.com/history.pdf",
            },
        )

        # Should not be 404 (route exists)
        assert response.status_code != 404

    def test_generate_reports_async_endpoint_exists(self, client):
        """Test that the async generate endpoint exists."""
        response = client.post(
            "/api/v1/patent-reports/generate/async",
            json={
                "patent_pdf_url": "https://example.com/patent.pdf",
                "history_pdf_url": "https://example.com/history.pdf",
            },
        )

        # Should not be 404 (route exists)
        assert response.status_code != 404

    def test_status_endpoint_not_found(self, client):
        """Test status endpoint returns 404 for unknown job."""
        response = client.get("/api/v1/patent-reports/status/unknown-job-id")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_generate_reports_validation_error(self, client):
        """Test validation error for missing required fields."""
        response = client.post(
            "/api/v1/patent-reports/generate",
            json={
                "patent_pdf_url": "https://example.com/patent.pdf",
                # Missing history_pdf_url
            },
        )

        assert response.status_code == 422  # Validation error

    @patch("src.api.routes.patent_reports.run_patent_pipeline")
    def test_generate_reports_success(self, mock_pipeline, client):
        """Test successful report generation."""
        mock_pipeline.return_value = {
            "status": "completed",
            "stage3_url": "https://example.com/stage3.md",
            "stage4_url": "https://example.com/stage4.md",
            "search_intel_url": "https://example.com/search_intel.md",
            "stage4_qc_json": {
                "metrics": {"overall_quality_score": 95.0}
            },
        }

        response = client.post(
            "/api/v1/patent-reports/generate",
            json={
                "patent_pdf_url": "https://example.com/patent.pdf",
                "history_pdf_url": "https://example.com/history.pdf",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["stage3_url"] == "https://example.com/stage3.md"
        assert data["stage4_url"] == "https://example.com/stage4.md"
        assert data["qc_score"] == 95.0

    @patch("src.api.routes.patent_reports.run_patent_pipeline")
    def test_generate_reports_pipeline_failure(self, mock_pipeline, client):
        """Test pipeline failure handling."""
        mock_pipeline.return_value = {
            "status": "failed",
            "error": "Stage 1 extraction failed",
        }

        response = client.post(
            "/api/v1/patent-reports/generate",
            json={
                "patent_pdf_url": "https://example.com/patent.pdf",
                "history_pdf_url": "https://example.com/history.pdf",
            },
        )

        assert response.status_code == 500
        assert "Stage 1 extraction failed" in response.json()["detail"]

    @patch("src.api.routes.patent_reports._run_pipeline_background")
    def test_generate_reports_async_returns_job_id(self, mock_bg, client):
        """Test async generation returns job ID."""
        response = client.post(
            "/api/v1/patent-reports/generate/async",
            json={
                "patent_pdf_url": "https://example.com/patent.pdf",
                "history_pdf_url": "https://example.com/history.pdf",
            },
        )

        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "pending"


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200


class TestOpenAPISchema:
    """Tests for OpenAPI schema generation."""

    def test_openapi_schema_includes_patent_reports(self, client):
        """Test that OpenAPI schema includes patent reports endpoints."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()

        # Check that patent reports paths exist
        paths = schema.get("paths", {})
        assert "/api/v1/patent-reports/generate" in paths
        assert "/api/v1/patent-reports/generate/async" in paths
        assert "/api/v1/patent-reports/status/{job_id}" in paths
