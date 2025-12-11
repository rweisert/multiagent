"""Extractor Agent - Stage 1 Record Extraction from PDFs."""

import json
import tempfile
import os
from typing import Any

import google.generativeai as genai
import structlog

from src.agents.base import AgentConfig, BaseAgent, LLMProvider

logger = structlog.get_logger(__name__)


class ExtractorAgent(BaseAgent):
    """Agent specialized in extracting structured data from patent PDFs.

    Uses Gemini for PDF processing capabilities.
    Corresponds to Stage 1 of the patent pipeline.
    """

    prompt_file = "PROMPT_Pipeline1_Stage1_RecordExtraction_v2.md"

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the extractor agent."""
        if config is None:
            config = AgentConfig(
                name="Extractor",
                role="Record extraction specialist - parses PDFs into structured JSON",
                provider=LLMProvider.GEMINI,
                temperature=0.1,  # Low temperature for precise extraction
                max_tokens=8192,
            )
        super().__init__(config)

    def _default_system_prompt(self) -> str:
        """Return the default system prompt for extraction."""
        return """You are a high-precision RECORD EXTRACTOR. Your job is to read patent PDFs
and convert them into well-structured JSON.

You are a PARSER, not an analyst. Extract verbatim text, normalize data structure,
and preserve exact quotes with pin-cites.

Do NOT analyze, interpret, or draw conclusions. Only extract what is in the record."""

    def _upload_pdf(self, pdf_bytes: bytes, display_name: str) -> Any:
        """Upload a PDF to Gemini for processing."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(pdf_bytes)
            temp_path = f.name

        try:
            uploaded_file = genai.upload_file(
                path=temp_path,
                display_name=display_name,
                mime_type="application/pdf",
            )
            logger.info("Uploaded PDF to Gemini", display_name=display_name)
            return uploaded_file
        finally:
            os.unlink(temp_path)

    def _parse_json_response(self, text: str) -> dict[str, Any]:
        """Parse JSON from LLM response."""
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            text = text[start:end].strip()

        return json.loads(text)

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Extract records from patent PDFs.

        Args:
            input_data: Dictionary containing:
                - history_pdf_bytes: Prosecution history PDF content
                - patent_pdf_bytes: Optional issued patent PDF content

        Returns:
            Dictionary with:
                - agent: Agent name
                - extraction: Extracted structured data as dict
                - status: "completed" or "failed"
                - error: Error message if failed
        """
        logger.info("Starting record extraction", agent=self.config.name)

        try:
            history_pdf_bytes = input_data.get("history_pdf_bytes")
            patent_pdf_bytes = input_data.get("patent_pdf_bytes")

            if not history_pdf_bytes:
                raise ValueError("history_pdf_bytes is required")

            # Upload PDFs
            history_file = self._upload_pdf(history_pdf_bytes, "prosecution_history.pdf")
            files = [history_file]

            if patent_pdf_bytes:
                patent_file = self._upload_pdf(patent_pdf_bytes, "issued_patent.pdf")
                files.append(patent_file)

            # Invoke with files
            response = await self.invoke(
                "Extract all records from the provided PDF files according to the schema.",
                files=files,
            )

            extraction = self._parse_json_response(response)

            logger.info(
                "Extraction completed",
                agent=self.config.name,
                events_count=len(extraction.get("events", [])),
                claims_count=len(extraction.get("claims_diff", [])),
            )

            return {
                "agent": self.config.name,
                "extraction": extraction,
                "status": "completed",
            }

        except Exception as e:
            logger.error("Extraction failed", agent=self.config.name, error=str(e))
            return {
                "agent": self.config.name,
                "extraction": {},
                "status": "failed",
                "error": str(e),
            }
