"""Search Intelligence node - Pipeline 2 sidecar."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient

logger = structlog.get_logger(__name__)


def search_intel_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Search Intelligence Module (Pipeline 2).

    This node:
    1. Generates search intelligence report based on Stage 1/2 data
    2. Updates state with search_intel_report_md

    Args:
        state: Pipeline state with stage1_extraction and stage2_forensic

    Returns:
        Updated state with search_intel_report_md
    """
    logger.info("Starting Search Intelligence Module")

    updates: dict = {}

    # Check for previous errors - but we can still try search intel
    # as it's a sidecar and doesn't block main pipeline
    if state.get("status") == "failed":
        logger.warning("Previous failure detected, attempting Search Intelligence anyway")

    try:
        # Check if we have required data
        stage1 = state.get("stage1_extraction")
        stage2_forensic = state.get("stage2_forensic")

        if not stage1 or not stage2_forensic:
            logger.warning("Missing required data for Search Intelligence")
            updates["search_intel_report_md"] = None
            return {**state, **updates}

        client = GeminiClient()

        # Extract data needed for search intel
        search_records = stage1.get("search_records", {})
        convergence_rows = stage2_forensic.get("convergence_rows", [])
        technical_reps = stage2_forensic.get("technical_reps", [])
        tech_pack_content = state.get("tech_pack_content", "")

        # Call Search Intelligence
        report_md = client.call_search_intel(
            search_records=search_records,
            convergence_rows=convergence_rows,
            technical_reps=technical_reps,
            tech_pack_content=tech_pack_content,
        )

        updates["search_intel_report_md"] = report_md

        logger.info(
            "Search Intelligence completed",
            report_length=len(report_md),
            report_lines=report_md.count("\n"),
        )

    except Exception as e:
        logger.error("Search Intelligence failed", error=str(e))
        # Don't fail the pipeline for search intel failure
        updates["search_intel_report_md"] = None
        logger.warning("Continuing pipeline without Search Intelligence report")

    return {**state, **updates}
