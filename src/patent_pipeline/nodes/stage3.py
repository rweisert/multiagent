"""Stage 3 node - Report Generation."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient

logger = structlog.get_logger(__name__)


def stage3_report_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Stage 3 - Report Generation.

    This node:
    1. Generates comprehensive litigation report from Stage 1 and 2 data
    2. Updates state with stage3_report_md

    Args:
        state: Pipeline state with stage1_extraction and stage2_forensic

    Returns:
        Updated state with stage3_report_md
    """
    logger.info("Starting Stage 3 - Report Generation")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 3 due to previous failure")
        return state

    try:
        client = GeminiClient()

        # Call Stage 3
        report_md = client.call_stage3(
            stage1_extraction=state["stage1_extraction"],
            stage2_forensic=state["stage2_forensic"],
        )

        updates["stage3_report_md"] = report_md

        logger.info(
            "Stage 3 completed",
            report_length=len(report_md),
            report_lines=report_md.count("\n"),
        )

    except Exception as e:
        logger.error("Stage 3 failed", error=str(e))
        updates["error"] = f"Stage 3 failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}
