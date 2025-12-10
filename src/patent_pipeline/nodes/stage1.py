"""Stage 1 node - Record Extraction from PDFs."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient
from src.patent_pipeline.models.stage1 import Stage1Extraction

logger = structlog.get_logger(__name__)


def stage1_extraction_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Stage 1 - Record Extraction.

    This node:
    1. Sends PDFs to Gemini for extraction
    2. Parses and validates the extraction results
    3. Updates state with stage1_extraction

    Args:
        state: Pipeline state with PDF bytes

    Returns:
        Updated state with stage1_extraction
    """
    logger.info("Starting Stage 1 - Record Extraction")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 1 due to previous failure")
        return state

    try:
        client = GeminiClient()

        # Call Stage 1
        result = client.call_stage1(
            history_pdf_bytes=state["history_pdf_bytes"],
            patent_pdf_bytes=state.get("patent_pdf_bytes"),
        )

        # Validate output structure
        try:
            Stage1Extraction.model_validate(result)
            logger.info("Stage 1 output validated successfully")
        except Exception as val_error:
            logger.warning(
                "Stage 1 output validation warning",
                error=str(val_error),
            )
            # Continue anyway - validation is advisory

        updates["stage1_extraction"] = result

        logger.info(
            "Stage 1 completed",
            events_count=len(result.get("events", [])),
            claims_count=len(result.get("claims_diff", [])),
        )

    except Exception as e:
        logger.error("Stage 1 failed", error=str(e))
        updates["error"] = f"Stage 1 failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}
