"""Tests for the patent litigation report pipeline."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.models.stage1 import Stage1Extraction, Stage1Metadata
from src.patent_pipeline.models.stage2 import Stage2A, Stage2B, Stage2C, Stage2Forensic
from src.patent_pipeline.models.stage4 import Stage4QC
from src.patent_pipeline.models.requests import GenerateReportRequest, GenerateReportResponse
from src.patent_pipeline.services.azure_io import (
    split_container_and_name,
    get_base_name,
)
from src.patent_pipeline.nodes.stage2_merge import stage2_merge_node
from src.patent_pipeline.nodes.tech_pack_router import tech_pack_router_node


class TestAzureIO:
    """Tests for Azure Blob I/O functions."""

    def test_split_container_and_name_basic(self):
        """Test splitting a basic blob URL."""
        url = "https://account.blob.core.windows.net/container/path/file.pdf"
        container_url, blob_name = split_container_and_name(url)

        assert container_url == "https://account.blob.core.windows.net/container"
        assert blob_name == "path/file.pdf"

    def test_split_container_and_name_with_sas(self):
        """Test splitting a blob URL with SAS token."""
        url = "https://account.blob.core.windows.net/container/file.pdf?sv=2021-06-08&sig=xxx"
        container_url, blob_name = split_container_and_name(url)

        assert "sv=2021-06-08" in container_url
        assert blob_name == "file.pdf"

    def test_split_container_and_name_nested_path(self):
        """Test splitting a blob URL with nested path."""
        url = "https://account.blob.core.windows.net/mycontainer/patents/2024/US12345.pdf"
        container_url, blob_name = split_container_and_name(url)

        assert container_url == "https://account.blob.core.windows.net/mycontainer"
        assert blob_name == "patents/2024/US12345.pdf"

    def test_split_container_and_name_invalid(self):
        """Test splitting an invalid blob URL."""
        url = "https://account.blob.core.windows.net/containeronly"

        with pytest.raises(ValueError):
            split_container_and_name(url)

    def test_get_base_name_simple(self):
        """Test extracting base name from simple blob URL."""
        url = "https://account.blob.core.windows.net/container/US12345678.pdf"
        base_name = get_base_name(url)

        assert base_name == "US12345678"

    def test_get_base_name_nested(self):
        """Test extracting base name from nested blob URL."""
        url = "https://account.blob.core.windows.net/container/patents/history/APPNO_wrapper.pdf"
        base_name = get_base_name(url)

        assert base_name == "APPNO_wrapper"


class TestPydanticModels:
    """Tests for Pydantic model validation."""

    def test_stage1_metadata_validation(self):
        """Test Stage1Metadata validation."""
        metadata = Stage1Metadata(
            application_number="16/123,456",
            title="Test Invention",
            inventors=["John Doe", "Jane Smith"],
        )

        assert metadata.application_number == "16/123,456"
        assert len(metadata.inventors) == 2

    def test_stage1_extraction_validation(self):
        """Test Stage1Extraction validation."""
        extraction = Stage1Extraction(
            metadata=Stage1Metadata(
                application_number="16/123,456",
                title="Test Invention",
            ),
            events=[],
            claims_diff=[],
        )

        assert extraction.metadata.application_number == "16/123,456"

    def test_stage2a_validation(self):
        """Test Stage2A validation."""
        stage2a = Stage2A(
            claim_construction_rows=[],
            estoppel_matrix_rows=[],
            construction_summary="Test summary",
        )

        assert stage2a.construction_summary == "Test summary"

    def test_stage4_qc_validation(self):
        """Test Stage4QC validation."""
        qc = Stage4QC(
            qc_issues=[],
            qc_summary="All checks passed",
            approved_for_delivery=True,
        )

        assert qc.approved_for_delivery is True

    def test_generate_report_request_validation(self):
        """Test GenerateReportRequest validation."""
        request = GenerateReportRequest(
            patent_pdf_url="https://account.blob.core.windows.net/container/patent.pdf",
            history_pdf_url="https://account.blob.core.windows.net/container/history.pdf",
        )

        assert "patent.pdf" in request.patent_pdf_url

    def test_generate_report_response_validation(self):
        """Test GenerateReportResponse validation."""
        response = GenerateReportResponse(
            stage3_url="https://account.blob.core.windows.net/container/report_stage3.md",
            stage4_url="https://account.blob.core.windows.net/container/report_stage4.md",
            search_intel_url=None,
            pipeline_status="completed",
            qc_score=95.5,
        )

        assert response.qc_score == 95.5
        assert response.search_intel_url is None


class TestStage2MergeNode:
    """Tests for Stage 2 Merge node."""

    def test_stage2_merge_basic(self):
        """Test basic Stage 2 merge functionality."""
        state: PatentPipelineState = {
            "stage2a": {
                "claim_construction_rows": [{"claim_number": 1}],
                "estoppel_matrix_rows": [{"claim_number": 1}],
                "construction_summary": "Summary A",
                "estoppel_summary": "Summary estoppel",
            },
            "stage2b": {
                "technical_reps": [{"rep_id": "TR-001"}],
                "search_gap_analysis": [],
                "convergence_rows": [{"convergence_id": "CONV-001"}],
                "technical_summary": "Summary B",
                "search_summary": "Search summary",
            },
            "stage2c": {
                "event_forensics": [{"event_date": "2024-01-01"}],
                "global_findings": {"key_vulnerabilities": []},
                "timeline_summary": "Summary C",
            },
        }

        result = stage2_merge_node(state)

        assert "stage2_forensic" in result
        forensic = result["stage2_forensic"]

        # Check all sections merged
        assert len(forensic["claim_construction_rows"]) == 1
        assert len(forensic["estoppel_matrix_rows"]) == 1
        assert len(forensic["technical_reps"]) == 1
        assert len(forensic["convergence_rows"]) == 1
        assert len(forensic["event_forensics"]) == 1
        assert forensic["global_findings"] is not None

    def test_stage2_merge_with_empty_sections(self):
        """Test Stage 2 merge with empty sections."""
        state: PatentPipelineState = {
            "stage2a": {},
            "stage2b": {},
            "stage2c": {},
        }

        result = stage2_merge_node(state)

        assert "stage2_forensic" in result
        forensic = result["stage2_forensic"]

        assert forensic["claim_construction_rows"] == []
        assert forensic["technical_reps"] == []
        assert forensic["event_forensics"] == []

    def test_stage2_merge_skips_on_failure(self):
        """Test Stage 2 merge skips when pipeline has failed."""
        state: PatentPipelineState = {
            "status": "failed",
            "error": "Previous error",
        }

        result = stage2_merge_node(state)

        assert result.get("status") == "failed"
        assert "stage2_forensic" not in result


class TestTechPackRouterNode:
    """Tests for Tech Pack Router node."""

    def test_tech_pack_router_from_tech_center(self):
        """Test routing from explicit tech center."""
        state: PatentPipelineState = {
            "stage1_extraction": {
                "metadata": {
                    "tech_center": "2100",
                    "art_unit": "2123",
                },
            },
        }

        with patch(
            "src.patent_pipeline.nodes.tech_pack_router.load_tech_pack"
        ) as mock_load:
            mock_load.return_value = "# Tech Pack Content"

            result = tech_pack_router_node(state)

            assert result["tech_center"] == "2100"
            assert result["tech_pack_content"] == "# Tech Pack Content"
            mock_load.assert_called_once_with("2100")

    def test_tech_pack_router_from_art_unit(self):
        """Test routing derived from art unit."""
        state: PatentPipelineState = {
            "stage1_extraction": {
                "metadata": {
                    "art_unit": "2634",  # Should derive TC 2600
                },
            },
        }

        with patch(
            "src.patent_pipeline.nodes.tech_pack_router.load_tech_pack"
        ) as mock_load:
            mock_load.return_value = "# Tech Pack Content"

            result = tech_pack_router_node(state)

            assert result["tech_center"] == "2600"

    def test_tech_pack_router_default(self):
        """Test routing defaults to TC 2100."""
        state: PatentPipelineState = {
            "stage1_extraction": {
                "metadata": {},
            },
        }

        with patch(
            "src.patent_pipeline.nodes.tech_pack_router.load_tech_pack"
        ) as mock_load:
            mock_load.return_value = "# Default Content"

            result = tech_pack_router_node(state)

            assert result["tech_center"] == "2100"

    def test_tech_pack_router_skips_on_failure(self):
        """Test router skips when pipeline has failed."""
        state: PatentPipelineState = {
            "status": "failed",
            "error": "Previous error",
        }

        result = tech_pack_router_node(state)

        assert result.get("status") == "failed"
        assert "tech_center" not in result


class TestPipelineState:
    """Tests for pipeline state structure."""

    def test_pipeline_state_structure(self):
        """Test that PatentPipelineState has expected keys."""
        state: PatentPipelineState = {
            "patent_pdf_url": "https://example.com/patent.pdf",
            "history_pdf_url": "https://example.com/history.pdf",
            "status": "pending",
        }

        assert state["patent_pdf_url"] == "https://example.com/patent.pdf"
        assert state["status"] == "pending"

    def test_pipeline_state_optional_fields(self):
        """Test that optional fields can be omitted."""
        state: PatentPipelineState = {
            "history_pdf_url": "https://example.com/history.pdf",
        }

        # Should not raise
        assert state.get("patent_pdf_url") is None
        assert state.get("tech_center") is None


class TestGeminiClient:
    """Tests for Gemini client (mocked)."""

    @patch("src.patent_pipeline.services.gemini_client.genai")
    def test_parse_json_response_basic(self, mock_genai):
        """Test JSON parsing from basic response."""
        from src.patent_pipeline.services.gemini_client import GeminiClient

        with patch.object(GeminiClient, "_load_prompts"):
            client = GeminiClient()

        test_json = '{"key": "value"}'
        result = client._parse_json_response(test_json)

        assert result == {"key": "value"}

    @patch("src.patent_pipeline.services.gemini_client.genai")
    def test_parse_json_response_with_markdown(self, mock_genai):
        """Test JSON parsing from markdown code block."""
        from src.patent_pipeline.services.gemini_client import GeminiClient

        with patch.object(GeminiClient, "_load_prompts"):
            client = GeminiClient()

        test_response = '''Here is the result:

```json
{"key": "value", "number": 42}
```

That's the output.'''

        result = client._parse_json_response(test_response)

        assert result == {"key": "value", "number": 42}
