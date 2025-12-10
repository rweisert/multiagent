"""Ingest PDFs node - downloads PDFs from Azure Blob Storage."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.azure_io import (
    download_blob,
    split_container_and_name,
    get_base_name,
)

logger = structlog.get_logger(__name__)


def ingest_pdfs_node(state: PatentPipelineState) -> PatentPipelineState:
    """Download patent and prosecution history PDFs from Azure.

    This node:
    1. Downloads the patent PDF (if URL provided)
    2. Downloads the prosecution history PDF
    3. Extracts Azure container URL and base name for later uploads

    Args:
        state: Pipeline state with patent_pdf_url and history_pdf_url

    Returns:
        Updated state with PDF bytes and Azure metadata
    """
    logger.info("Starting PDF ingestion")

    updates: dict = {"status": "processing"}

    try:
        # Download patent PDF
        patent_url = state.get("patent_pdf_url")
        if patent_url:
            logger.info("Downloading patent PDF")
            updates["patent_pdf_bytes"] = download_blob(patent_url)
            logger.info(
                "Patent PDF downloaded",
                size_bytes=len(updates["patent_pdf_bytes"]),
            )

        # Download prosecution history PDF (required)
        history_url = state["history_pdf_url"]
        logger.info("Downloading prosecution history PDF")
        updates["history_pdf_bytes"] = download_blob(history_url)
        logger.info(
            "History PDF downloaded",
            size_bytes=len(updates["history_pdf_bytes"]),
        )

        # Extract Azure metadata from history URL for later uploads
        container_url, blob_name = split_container_and_name(history_url)
        updates["azure_container_url"] = container_url
        updates["base_name"] = get_base_name(history_url)

        logger.info(
            "PDF ingestion completed",
            container_url=container_url,
            base_name=updates["base_name"],
        )

    except Exception as e:
        logger.error("PDF ingestion failed", error=str(e))
        updates["error"] = f"PDF ingestion failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}
